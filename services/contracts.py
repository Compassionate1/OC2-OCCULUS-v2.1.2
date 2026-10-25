import json, math, uuid
from datetime import datetime, timezone
KINDS = {'visual','audio','fused','attention','prediction','validation'}
def validate_event(obj):
    required = ('event_id','event_time','source_id','mode','event_type','schema_version','payload')
    if not isinstance(obj,dict) or any(k not in obj for k in required):
        raise ValueError('missing required event fields')
    uuid.UUID(obj['event_id'])
    ts = datetime.fromisoformat(obj['event_time'].replace('Z','+00:00'))
    if ts.tzinfo is None: raise ValueError('timestamp must include timezone')
    if obj['mode'] not in ('simulation','live'): raise ValueError('invalid mode')
    if obj['event_type'] not in KINDS: raise ValueError('invalid event type')
    if obj['schema_version'] != 'oc2.event.v1': raise ValueError('invalid schema')
    if not isinstance(obj['payload'],dict): raise ValueError('payload must be object')
    if not isinstance(obj['source_id'],str) or not obj['source_id'] or len(obj['source_id'])>128: raise ValueError('invalid source')
    for field in ('bearing_deg','confidence'):
        if field in obj and (not isinstance(obj[field],(int,float)) or not math.isfinite(obj[field])):
            raise ValueError('nonfinite numeric field')
    if 'confidence' in obj and not 0<=obj['confidence']<=1: raise ValueError('confidence outside range')
    return obj

def new_event(source_id,mode,event_type,payload,bearing_deg=None,confidence=None,event_time=None):
    e={'event_id':str(uuid.uuid4()),'event_time':event_time or datetime.now(timezone.utc).isoformat(),
       'source_id':source_id,'mode':mode,'event_type':event_type,'schema_version':'oc2.event.v1','payload':payload}
    if bearing_deg is not None:e['bearing_deg']=bearing_deg
    if confidence is not None:e['confidence']=confidence
    return validate_event(e)
