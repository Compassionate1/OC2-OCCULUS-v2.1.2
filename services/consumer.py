"""Kafka-to-TimescaleDB consumer with explicit commit ordering."""

from __future__ import annotations

import json
import logging
import os
import time
from typing import Any

from .contracts import validate_event
from .store import save_event

LOGGER = logging.getLogger("oc2.consumer")
TOPIC = "oc2.events.v1"
GROUP_ID = "oc2-timescale-writer-v2"


def _consumer(broker: str) -> Any:
    from kafka import KafkaConsumer

    return KafkaConsumer(
        TOPIC,
        bootstrap_servers=broker,
        group_id=GROUP_ID,
        enable_auto_commit=False,
        auto_offset_reset="earliest",
        value_deserializer=lambda raw: json.loads(raw.decode("utf-8")),
        consumer_timeout_ms=0,
    )


def run_once(database_url: str, broker: str) -> None:
    import psycopg

    consumer = _consumer(broker)
    try:
        with psycopg.connect(database_url) as connection:
            for message in consumer:
                try:
                    event = validate_event(message.value)
                    save_event(connection, event)
                    connection.commit()
                    consumer.commit()
                except Exception:
                    connection.rollback()
                    LOGGER.exception("consumer rejected event; offset not committed")
                    raise
    finally:
        consumer.close()


def main() -> None:
    logging.basicConfig(level=os.getenv("OC2_LOG_LEVEL", "INFO"), format="%(asctime)s %(levelname)s %(name)s %(message)s")
    database_url = os.environ["OC2_DATABASE_URL"]
    broker = os.getenv("OC2_KAFKA_BOOTSTRAP", "kafka:9092")
    while True:
        try:
            run_once(database_url, broker)
        except KeyboardInterrupt:
            return
        except Exception as exc:
            LOGGER.warning("consumer reconnect after %s", type(exc).__name__)
            time.sleep(3.0)


if __name__ == "__main__":
    main()
