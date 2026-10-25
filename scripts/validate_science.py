#!/usr/bin/env python3
"""Independent synthetic prediction acceptance check, distinct from real-world validation."""
import argparse,json,math
from pathlib import Path

def circular_error(a,b):return abs((a-b+180)%360-180)
def validate(rows,max_rmse=15,min_coverage=.9):
    if not rows:raise ValueError('No ground-truth observations')
    errors=[];covered=0
    for r in rows:
        truth=float(r['truth_deg']);prediction=float(r['prediction_deg']);halfwidth=float(r['interval_halfwidth_deg'])
        if not all(map(math.isfinite,(truth,prediction,halfwidth))) or not 0<=halfwidth<=180:raise ValueError('Invalid angular observation')
        e=circular_error(truth,prediction);errors.append(e);covered+=e<=halfwidth
    rmse=math.sqrt(sum(e*e for e in errors)/len(errors));coverage=covered/len(errors)
    return {'schema':'oc2.scientific-acceptance.v1','n':len(rows),'angular_rmse_deg':round(rmse,6),'interval_coverage':round(coverage,6),'thresholds':{'max_rmse_deg':max_rmse,'min_coverage':min_coverage},'passed':rmse<=max_rmse and coverage>=min_coverage,'scope':'synthetic data only'}
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('input');ap.add_argument('--output',required=True);ap.add_argument('--max-rmse',type=float,default=15);ap.add_argument('--min-coverage',type=float,default=.9);a=ap.parse_args()
    out=validate(json.loads(Path(a.input).read_text()),a.max_rmse,a.min_coverage);Path(a.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out));raise SystemExit(0 if out['passed'] else 1)
