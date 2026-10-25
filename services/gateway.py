import json,os,time
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse
from .contracts import validate_event
from .simulator import simulate
from .store import save_event
from kafka import KafkaProducer, KafkaConsumer
import psycopg

TOKEN=os.getenv('OC2_API_TOKEN','local-demo-token-change-me')
BOOTSTRAP=os.getenv('OC2_KAFKA_BOOTSTRAP','kafka:9092')
DB=os.getenv('OC2_DATABASE_URL')
ROOT=Path('/app/web')
TOPIC='oc2.events.v1'

def producer():
    for attempt in range(30):
        try: return KafkaProducer(bootstrap_servers=BOOTSTRAP,value_serializer=lambda e:json.dumps(e,separators=(',',':')).encode(),acks='all',retries=5)
        except Exception:
            if attempt==29:raise
            time.sleep(2)

class Handler(BaseHTTPRequestHandler):
    def respond(self,status,body,content='application/json'):
        data=body if isinstance(body,bytes) else body.encode()
        self.send_response(status);self.send_header('Content-Type',content);self.send_header('Content-Length',str(len(data)));self.send_header('Cache-Control','no-store');self.end_headers();self.wfile.write(data)
    def authorized(self): return self.headers.get('Authorization')=='Bearer '+TOKEN
    def do_GET(self):
        path=urlparse(self.path).path
        if path=='/health':return self.respond(200,'{"status":"ok","version":"2.0.2"}')
        if path=='/':return self.respond(200,(ROOT/'index.html').read_bytes(),'text/html; charset=utf-8')
        if not self.authorized():return self.respond(401,'{"error":"unauthorized"}')
        if path=='/api/recent':
            with psycopg.connect(DB) as conn:
                rows=conn.execute('SELECT event_id::text,event_time::text,source_id,mode,event_type,bearing_deg,confidence,payload FROM oc2_events ORDER BY event_time DESC LIMIT 150').fetchall()
            data=[dict(zip(('event_id','event_time','source_id','mode','event_type','bearing_deg','confidence','payload'),r)) for r in rows]
            return self.respond(200,json.dumps(data))
        if path=='/api/stats':
            with psycopg.connect(DB) as conn:
                rows=conn.execute('SELECT event_type,count(*) FROM oc2_events GROUP BY event_type').fetchall()
            return self.respond(200,json.dumps(dict(rows)))
        return self.respond(404,'{"error":"not found"}')
    def do_POST(self):
        if not self.authorized():return self.respond(401,'{"error":"unauthorized"}')
        path=urlparse(self.path).path
        if path not in ('/api/events','/api/seed'):return self.respond(404,'{"error":"not found"}')
        try:
            n=int(self.headers.get('Content-Length','0'))
            if n<0 or n>1048576:raise ValueError('invalid content length')
            obj=json.loads(self.rfile.read(n)) if path=='/api/events' else {}
            events=[validate_event(obj)] if path=='/api/events' else list(simulate(seed=2026,steps=60,objects=3))
            p=producer()
            for e in events:
                p.send(TOPIC,key=e['source_id'].encode(),value=e).get(timeout=15)
            p.flush(timeout=15);p.close()
            return self.respond(202,json.dumps({'accepted':len(events),'broker':'kafka'}))
        except (ValueError,TypeError,json.JSONDecodeError) as exc:
            return self.respond(400,json.dumps({'error':str(exc)}))
        except Exception:
            return self.respond(503,'{"error":"broker unavailable"}')

if __name__=='__main__':
    ThreadingHTTPServer(('0.0.0.0',8088),Handler).serve_forever()
