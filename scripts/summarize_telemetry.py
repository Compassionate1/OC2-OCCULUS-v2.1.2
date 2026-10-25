#!/usr/bin/env python3
"""Summarize measured executions; do not infer DORA metrics from local test runs."""
import argparse,json,statistics
from pathlib import Path

def summarize(path):
 rows=[json.loads(x) for x in Path(path).read_text().splitlines() if x.strip()]
 if not rows:return {'observations':0,'note':'No observed measurements'}
 durations=sorted(float(r['duration_seconds']) for r in rows)
 return {'observations':len(rows),'pass_count':sum(r['exit_code']==0 for r in rows),
  'fail_count':sum(r['exit_code']!=0 for r in rows),
  'median_duration_seconds':statistics.median(durations),
  'p90_duration_seconds':durations[max(0,__import__('math').ceil(.9*len(durations))-1)],
  'commit_shas':sorted({r['commit_sha'] for r in rows if r.get('commit_sha')}),
  'scope':'execution telemetry only; deployment/incident metrics require event sources'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('input');p.add_argument('--output');a=p.parse_args()
 result=json.dumps(summarize(a.input),indent=2)+'\n'
 if a.output:Path(a.output).write_text(result)
 else:print(result,end='')
