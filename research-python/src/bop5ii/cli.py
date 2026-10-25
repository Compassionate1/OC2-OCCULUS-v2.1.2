"""Command-line entry point."""
import argparse,csv,json,pathlib
from dataclasses import asdict
from .model import Config,run
from .validation import summarize,bootstrap_rmse,by_snr

def main(argv=None):
    p=argparse.ArgumentParser(description='BOP5ii v1.0.0 — RESTRICTED (user-defined), synthetic only')
    p.add_argument('--trajectories',type=int,default=100)
    p.add_argument('--steps',type=int,default=60)
    p.add_argument('--seed',type=int,default=52)
    p.add_argument('--occlusion',type=float,default=.24)
    p.add_argument('--output',default='artifacts')
    args=p.parse_args(argv)
    cfg=Config(trajectories=args.trajectories,steps=args.steps,seed=args.seed,occlusion_probability=args.occlusion)
    rows=run(cfg)
    # Separate independent trajectory IDs for holdout; no temporal row leakage.
    split=max(1,int(.8*cfg.trajectories))
    train=[r for r in rows if r.trajectory<split]
    test=[r for r in rows if r.trajectory>=split]
    result={'project':'BOP5ii','version':'1.0.0','marking':'RESTRICTED — USER-DEFINED / NOT GOVERNMENT CLASSIFIED','synthetic_only':True,'config':asdict(cfg),'train_diagnostics':summarize(train),'holdout':summarize(test),'holdout_by_snr':by_snr(test),'holdout_rmse_bootstrap_95':bootstrap_rmse(test),'gates':{}}
    h=result['holdout']
    result['gates']={'rmse_le_8deg':h['angular_rmse_deg']<=8,'coverage_90_to_99pct':.90<=h['interval_95_coverage']<=.99,'brier_le_0_15':h['aperture_brier']<=.15,'recognition_f1_ge_0_65':h['recognition_macro_f1']>=.65,'recognition_ece_le_0_15':h['recognition_ece']<=.15}
    result['release_gate_pass']=all(result['gates'].values())
    out=pathlib.Path(args.output);out.mkdir(parents=True,exist_ok=True)
    with (out/'observations.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0].as_row()));w.writeheader();w.writerows(r.as_row() for r in rows)
    (out/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'holdout':h,'gates':result['gates'],'release_gate_pass':result['release_gate_pass']},indent=2))
    return 0
if __name__=='__main__':raise SystemExit(main())
