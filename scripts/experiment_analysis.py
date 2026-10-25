#!/usr/bin/env python3
"""Pre-registered A/B process experiment analysis; independent observations assumed."""
import argparse,json,math,random,statistics
from pathlib import Path

def analyze(baseline,treatment,iterations=2000,seed=202603):
    if len(baseline)<5 or len(treatment)<5:raise ValueError('At least five observations per arm required')
    if any(not math.isfinite(x) or x<0 for x in baseline+treatment):raise ValueError('Durations must be finite nonnegative')
    rng=random.Random(seed); delta=statistics.mean(baseline)-statistics.mean(treatment)
    draws=[]
    for _ in range(iterations):
        b=[rng.choice(baseline) for _ in baseline];t=[rng.choice(treatment) for _ in treatment]
        draws.append(statistics.mean(b)-statistics.mean(t))
    draws.sort();lo=draws[int(.025*(iterations-1))];hi=draws[int(.975*(iterations-1))]
    return {'schema':'oc2.experiment.v1','baseline_n':len(baseline),'treatment_n':len(treatment),'mean_reduction_seconds':round(delta,6),'bootstrap_95_ci_seconds':[round(lo,6),round(hi,6)],'improvement_supported':lo>0,'seed':seed,'iterations':iterations,'limitations':'Bootstrap assumes independent representative observations; randomization and pre-registration must be independently documented.'}
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('input');ap.add_argument('--output',required=True);a=ap.parse_args();d=json.loads(Path(a.input).read_text());Path(a.output).write_text(json.dumps(analyze(d['baseline'],d['treatment']),indent=2)+'\n')
