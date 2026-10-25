import json,os,time
import psycopg
from kafka import KafkaConsumer
from .contracts import validate_event
from .store import save_event

def main():
    db=os.environ['OC2_DATABASE_URL'];broker=os.getenv('OC2_KAFKA_BOOTSTRAP','kafka:9092')
    while True:
        try:
            consumer=KafkaConsumer('oc2.events.v1',bootstrap_servers=broker,group_id='oc2-timescale-writer-v1',enable_auto_commit=False,auto_offset_reset='earliest',value_deserializer=lambda x:json.loads(x))
            with psycopg.connect(db) as conn:
                for message in consumer:
                    try:
                        save_event(conn,validate_event(message.value))
                        consumer.commit()
                    except Exception as exc:
                        conn.rollback();print('consumer rejected event',exc,flush=True)
                        # halt instead of silently discarding poison messages
                        raise
        except Exception as exc:
            print('consumer reconnect',str(exc),flush=True);time.sleep(3)
if __name__=='__main__':main()
