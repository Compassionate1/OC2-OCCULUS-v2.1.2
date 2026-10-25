#!/usr/bin/env python3
"""Live stack smoke: send seed request and check DB persistence; requires docker compose."""
import argparse,json,os,subprocess,time,urllib.request

def run(url,token,timeout):
 req=urllib.request.Request(url.rstrip('/')+'/api/seed',data=b'{}',method='POST',headers={'Authorization':'Bearer '+token,'Content-Type':'application/json'})
 with urllib.request.urlopen(req,timeout=15) as response:
  if response.status not in (200,201,202):raise RuntimeError('seed endpoint HTTP '+str(response.status))
  payload=json.loads(response.read())
 deadline=time.monotonic()+timeout
 while time.monotonic()<deadline:
  sql='SELECT count(*) FROM oc2_events;' # update only after checking actual schema
  query=subprocess.run(['docker','compose','exec','-T','timescaledb','psql','-U','oc2','-d','oc2','-tAc',sql],capture_output=True,text=True)
  if query.returncode==0 and query.stdout.strip().isdigit() and int(query.stdout.strip())>0:
   print(json.dumps({'status':'passed','observation_count':int(query.stdout.strip()),'seed_response':payload}));return
  time.sleep(2)
 raise RuntimeError('No persisted observations before timeout; inspect consumer logs and schema')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--url',default='http://127.0.0.1:8088');p.add_argument('--token',default=os.getenv('OC2_API_TOKEN',''))
 p.add_argument('--timeout',type=int,default=90);a=p.parse_args()
 if not a.token:p.error('set OC2_API_TOKEN or --token')
 run(a.url,a.token,a.timeout)
