"""Persistence adapter for TimescaleDB/PostgreSQL."""

from __future__ import annotations

import json
from typing import Any

INSERT_SQL = """
INSERT INTO oc2_events(
    event_id, event_time, source_id, mode, event_type,
    schema_version, bearing_deg, confidence, payload
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s::jsonb)
ON CONFLICT DO NOTHING
"""


def save_event(connection: Any, event: dict[str, Any], *, commit: bool = False) -> None:
    """Persist one validated event; transaction ownership defaults to the caller."""
    values = (
        event["event_id"],
        event["event_time"],
        event["source_id"],
        event["mode"],
        event["event_type"],
        event["schema_version"],
        event.get("bearing_deg"),
        event.get("confidence"),
        json.dumps(event["payload"], separators=(",", ":"), sort_keys=True),
    )
    with connection.cursor() as cursor:
        cursor.execute(INSERT_SQL, values)
    if commit:
        connection.commit()
