import json
SQL='INSERT INTO oc2_events(event_id,event_time,source_id,mode,event_type,schema_version,bearing_deg,confidence,payload) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s::jsonb) ON CONFLICT DO NOTHING'
def save_event(conn,e):
    with conn.cursor() as cur:
        cur.execute(SQL,(e['event_id'],e['event_time'],e['source_id'],e['mode'],e['event_type'],e['schema_version'],e.get('bearing_deg'),e.get('confidence'),json.dumps(e['payload'])))
    conn.commit()
