"""Holdout evaluation and trajectory-block bootstrap intervals."""
import math
import random
from collections import defaultdict
from .model import wrap

def summarize(rows):
    n=len(rows)
    if not n:
        raise ValueError('empty evaluation sample')
    errors=[wrap(r.predicted_bearing-r.true_bearing) for r in rows]
    rmse=math.sqrt(sum(x*x for x in errors)/n)
    mae=sum(abs(x) for x in errors)/n
    cover=sum(abs(e)<=1.96*r.predicted_sd for e,r in zip(errors,rows))/n
    brier=sum((r.aperture_probability-r.aperture_event)**2 for r in rows)/n
    accuracy=sum(r.predicted_class==r.actual_class for r in rows)/n
    precision=[];recall=[];f1=[]
    for cls in sorted({r.actual_class for r in rows}):
        tp=sum(r.actual_class==cls and r.predicted_class==cls for r in rows)
        fp=sum(r.actual_class!=cls and r.predicted_class==cls for r in rows)
        fn=sum(r.actual_class==cls and r.predicted_class!=cls for r in rows)
        p=tp/(tp+fp) if tp+fp else 0
        rec=tp/(tp+fn) if tp+fn else 0
        precision.append(p);recall.append(rec);f1.append(2*p*rec/(p+rec) if p+rec else 0)
    tp=sum(r.change_truth and r.change_detected for r in rows)
    fp=sum(not r.change_truth and r.change_detected for r in rows)
    fn=sum(r.change_truth and not r.change_detected for r in rows)
    tn=sum(not r.change_truth and not r.change_detected for r in rows)
    bins=[]
    for i in range(10):
        b=[r for r in rows if min(9,int(r.recognition_confidence*10))==i]
        if b:
            bins.append({'n':len(b),'confidence':sum(r.recognition_confidence for r in b)/len(b),'accuracy':sum(r.actual_class==r.predicted_class for r in b)/len(b)})
    ece=sum(b['n']/n*abs(b['confidence']-b['accuracy']) for b in bins)
    return {'n':n,'trajectories':len(set(r.trajectory for r in rows)),'angular_rmse_deg':rmse,'angular_mae_deg':mae,'interval_95_coverage':cover,'aperture_brier':brier,'recognition_accuracy':accuracy,'recognition_macro_f1':sum(f1)/len(f1),'recognition_ece':ece,'recognition_reliability_bins':bins,'change_precision':tp/(tp+fp) if tp+fp else 0,'change_recall':tp/(tp+fn) if tp+fn else 0,'change_false_alarm_rate':fp/(fp+tn) if fp+tn else 0,'audio_ambiguity_rate':sum(r.ambiguous for r in rows)/n,'visual_occlusion_rate':sum(r.occluded for r in rows)/n}

def bootstrap_rmse(rows, repetitions=300, seed=37):
    by=defaultdict(list)
    for row in rows:by[row.trajectory].append(row)
    keys=list(by)
    rng=random.Random(seed)
    values=[]
    for _ in range(repetitions):
        sample=[]
        for _ in keys: sample.extend(by[rng.choice(keys)])
        values.append(summarize(sample)['angular_rmse_deg'])
    values.sort()
    return [values[int(.025*(repetitions-1))],values[int(.975*(repetitions-1))]]

def by_snr(rows):
    return {name:summarize([r for r in rows if lo<=r.snr_db<hi]) for name,lo,hi in [('low',-100,0),('medium',0,10),('high',10,100)] if any(lo<=r.snr_db<hi for r in rows)}
