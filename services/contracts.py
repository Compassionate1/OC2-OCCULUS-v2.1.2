"""OC2 event contract creation and validation."""

from __future__ import annotations

from datetime import datetime, timezone
import math
from typing import Any, Final
from uuid import UUID, uuid4

SCHEMA_VERSION: Final = "oc2.event.v1"
EVENT_KINDS: Final[frozenset[str]] = frozenset({"visual", "audio", "fused", "attention", "prediction", "validation"})
MODES: Final[frozenset[str]] = frozenset({"simulation", "live"})
MAX_SOURCE_ID_LENGTH: Final = 128


def _parse_timestamp(value: str) -> datetime:
    timestamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if timestamp.tzinfo is None or timestamp.utcoffset() is None:
        raise ValueError("event_time must include a UTC offset")
    return timestamp


def validate_event(obj: object) -> dict[str, Any]:
    """Validate an OC2 event and return it unchanged when valid."""
    if not isinstance(obj, dict):
        raise ValueError("event must be a JSON object")
    required = {"event_id", "event_time", "source_id", "mode", "event_type", "schema_version", "payload"}
    missing = sorted(required.difference(obj))
    if missing:
        raise ValueError(f"missing required event fields: {', '.join(missing)}")

    UUID(str(obj["event_id"]))
    _parse_timestamp(str(obj["event_time"]))

    source_id = obj["source_id"]
    if not isinstance(source_id, str) or not source_id or len(source_id) > MAX_SOURCE_ID_LENGTH:
        raise ValueError("source_id must be a non-empty string <= 128 characters")
    if obj["mode"] not in MODES:
        raise ValueError("invalid mode")
    if obj["event_type"] not in EVENT_KINDS:
        raise ValueError("invalid event_type")
    if obj["schema_version"] != SCHEMA_VERSION:
        raise ValueError("invalid schema_version")
    if not isinstance(obj["payload"], dict):
        raise ValueError("payload must be an object")

    for field in ("bearing_deg", "confidence"):
        if field in obj:
            value = obj[field]
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(float(value)):
                raise ValueError(f"{field} must be finite numeric data")
    if "confidence" in obj and not 0.0 <= float(obj["confidence"]) <= 1.0:
        raise ValueError("confidence must be in [0, 1]")
    return obj


def new_event(
    source_id: str,
    mode: str,
    event_type: str,
    payload: dict[str, Any],
    bearing_deg: float | None = None,
    confidence: float | None = None,
    event_time: str | None = None,
) -> dict[str, Any]:
    event: dict[str, Any] = {
        "event_id": str(uuid4()),
        "event_time": event_time or datetime.now(timezone.utc).isoformat(),
        "source_id": source_id,
        "mode": mode,
        "event_type": event_type,
        "schema_version": SCHEMA_VERSION,
        "payload": payload,
    }
    if bearing_deg is not None:
        event["bearing_deg"] = float(bearing_deg)
    if confidence is not None:
        event["confidence"] = float(confidence)
    return validate_event(event)
