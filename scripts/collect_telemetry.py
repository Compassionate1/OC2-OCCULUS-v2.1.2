#!/usr/bin/env python3
"""Collect reproducible local/GitHub Actions execution measurements (no GitHub API token needed)."""
import argparse,datetime as dt,json,os,subprocess,time,uuid
from pathlib import Path

def git(*args):
 try:return subprocess.check_output(['git',*args],stderr=subprocess.DEVNULL,text=True).strip()
 except (OSError,subprocess.CalledProcessError):return None

def measure(command,output,phase='test'):
 start=time.time(); mono=time.perf_counter()
 proc=subprocess.run(command,check=False)
 end=time.time()
 record={'schema':'oc2.telemetry.v1','id':str(uuid.uuid4()),'phase':phase,'command':command,
  'started_at':dt.datetime.fromtimestamp(start,dt.timezone.utc).isoformat(),
  'finished_at':dt.datetime.fromtimestamp(end,dt.timezone.utc).isoformat(),
  'duration_seconds':round(time.perf_counter()-mono,6),'exit_code':proc.returncode,
  'commit_sha':git('rev-parse','HEAD'),'branch':git('branch','--show-current'),
  'github_run_id':os.getenv('GITHUB_RUN_ID'),'github_run_attempt':os.getenv('GITHUB_RUN_ATTEMPT'),
  'github_workflow':os.getenv('GITHUB_WORKFLOW'),'github_ref':os.getenv('GITHUB_REF'),
  'environment':os.getenv('RUNNER_OS','local')}
 p=Path(output);p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('a') as f:f.write(json.dumps(record,sort_keys=True)+'\n')
 return proc.returncode

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--output',default='artifacts/telemetry/measurements.jsonl')
 parser.add_argument('--phase',default='test');parser.add_argument('command',nargs=argparse.REMAINDER)
 args=parser.parse_args();cmd=args.command[1:] if args.command[:1]==['--'] else args.command
 if not cmd:parser.error('command required after --')
 raise SystemExit(measure(cmd,args.output,args.phase))
