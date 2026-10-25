#!/usr/bin/env python3
"""Derive process performance baselines from real OC2 JSONL telemetry; never invent observations."""
import argparse, json, math, statistics
from pathlib import Path

def quantile(values, p):
    if not values: return None
    a=sorted(values); x=(len(a)-1)*p; lo=math.floor(x); hi=math.ceil(x)
    return round(a[lo]+(a[hi]-a[lo])*(x-lo),6)

def summarize(rows, min_n=20):
    phases=sorted({r.get('phase','unknown') for r in rows})
    out={'schema':'oc2.process-baseline.v1','sample_count':len(rows),'minimum_samples':min_n,'phases':{}}
    for phase in phases:
        group=[r for r in rows if r.get('phase','unknown')==phase]
        valid=[float(r['duration_seconds']) for r in group if isinstance(r.get('duration_seconds'),(int,float)) and math.isfinite(r['duration_seconds']) and r['duration_seconds']>=0]
        passed=sum(r.get('exit_code')==0 for r in group)
        out['phases'][phase]={'n':len(group),'valid_duration_n':len(valid),'pass_rate':round(passed/len(group),6),'p50_seconds':quantile(valid,.5),'p90_seconds':quantile(valid,.9),'mean_seconds':round(statistics.mean(valid),6) if valid else None,'stdev_seconds':round(statistics.stdev(valid),6) if len(valid)>1 else None,'baseline_eligible':len(valid)>=min_n}
    out['predictive_model']='not_fitted' if not any(x['baseline_eligible'] for x in out['phases'].values()) else 'eligible_for_holdout_validation'
    return out

def main():
    a=argparse.ArgumentParser();a.add_argument('inputs',nargs='+');a.add_argument('--output',required=True);a.add_argument('--minimum-samples',type=int,default=20);args=a.parse_args()
    rows=[]
    for f in args.inputs:
        for line in Path(f).read_text().splitlines():
            if line.strip():rows.append(json.loads(line))
    out=summarize(rows,args.minimum_samples);dest=Path(args.output);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
