"""Minimal authenticated HTTP ingestion/read gateway for OC2."""

from __future__ import annotations

from dataclasses import dataclass
import hmac
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import time
from typing import Any, Final
from urllib.parse import urlparse

from .contracts import validate_event
from .simulator import simulate

VERSION: Final = "2.1.3"
TOPIC: Final = "oc2.events.v1"
MAX_REQUEST_BYTES: Final = 1_048_576
ROOT: Final = Path(os.getenv("OC2_WEB_ROOT", "/app/web"))


@dataclass(frozen=True, slots=True)
class Settings:
    api_token: str
    kafka_bootstrap: str
    database_url: str

    @classmethod
    def from_environment(cls) -> "Settings":
        token = os.getenv("OC2_API_TOKEN", "")
        database_url = os.getenv("OC2_DATABASE_URL", "")
        if not token:
            raise RuntimeError("OC2_API_TOKEN must be configured")
        if not database_url:
            raise RuntimeError("OC2_DATABASE_URL must be configured")
        return cls(token, os.getenv("OC2_KAFKA_BOOTSTRAP", "kafka:9092"), database_url)


def _json_bytes(value: object) -> bytes:
    return json.dumps(value, separators=(",", ":"), sort_keys=True).encode("utf-8")


def create_producer(settings: Settings) -> Any:
    from kafka import KafkaProducer

    for attempt in range(30):
        try:
            return KafkaProducer(
                bootstrap_servers=settings.kafka_bootstrap,
                acks="all",
                retries=5,
                request_timeout_ms=15_000,
            )
        except Exception:
            if attempt == 29:
                raise
            time.sleep(2.0)
    raise AssertionError("unreachable")


class Handler(BaseHTTPRequestHandler):
    server_version = "OC2Gateway/2.1.3"

    @property
    def settings(self) -> Settings:
        return self.server.settings  # type: ignore[attr-defined]

    def log_message(self, format: str, *args: object) -> None:
        print(json.dumps({"component": "gateway", "client": self.client_address[0], "message": format % args}), flush=True)

    def _respond(self, status: int, body: bytes | str | object, content_type: str = "application/json") -> None:
        if isinstance(body, bytes):
            data = body
        elif isinstance(body, str):
            data = body.encode("utf-8")
        else:
            data = _json_bytes(body)
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(data)

    def _authorized(self) -> bool:
        expected = f"Bearer {self.settings.api_token}"
        supplied = self.headers.get("Authorization", "")
        return hmac.compare_digest(supplied, expected)

    def _read_json(self) -> dict[str, Any]:
        raw_length = self.headers.get("Content-Length")
        if raw_length is None:
            raise ValueError("Content-Length required")
        length = int(raw_length)
        if not 0 <= length <= MAX_REQUEST_BYTES:
            raise ValueError("invalid Content-Length")
        payload = json.loads(self.rfile.read(length))
        if not isinstance(payload, dict):
            raise ValueError("request body must be a JSON object")
        return payload

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path == "/health":
            self._respond(200, {"status": "ok", "version": VERSION})
            return
        if path == "/":
            index = ROOT / "index.html"
            if not index.is_file():
                self._respond(404, {"error": "web asset unavailable"})
                return
            self._respond(200, index.read_bytes(), "text/html; charset=utf-8")
            return
        if not self._authorized():
            self._respond(401, {"error": "unauthorized"})
            return

        import psycopg

        if path == "/api/recent":
            with psycopg.connect(self.settings.database_url) as connection:
                rows = connection.execute(
                    "SELECT event_id::text,event_time::text,source_id,mode,event_type,bearing_deg,confidence,payload "
                    "FROM oc2_events ORDER BY event_time DESC LIMIT 150"
                ).fetchall()
            columns = ("event_id", "event_time", "source_id", "mode", "event_type", "bearing_deg", "confidence", "payload")
            self._respond(200, [dict(zip(columns, row, strict=True)) for row in rows])
            return
        if path == "/api/stats":
            with psycopg.connect(self.settings.database_url) as connection:
                rows = connection.execute("SELECT event_type,count(*) FROM oc2_events GROUP BY event_type").fetchall()
            self._respond(200, dict(rows))
            return
        self._respond(404, {"error": "not found"})

    def do_POST(self) -> None:
        if not self._authorized():
            self._respond(401, {"error": "unauthorized"})
            return
        path = urlparse(self.path).path
        if path not in {"/api/events", "/api/seed"}:
            self._respond(404, {"error": "not found"})
            return
        try:
            events = [validate_event(self._read_json())] if path == "/api/events" else list(simulate(seed=2026, steps=60, objects=3))
            producer = create_producer(self.settings)
            try:
                for event in events:
                    producer.send(
                        TOPIC,
                        key=str(event["source_id"]).encode("utf-8"),
                        value=_json_bytes(event),
                    ).get(timeout=15)
                producer.flush(timeout=15)
            finally:
                producer.close(timeout=15)
            self._respond(202, {"accepted": len(events), "broker": "kafka"})
        except (ValueError, TypeError, json.JSONDecodeError) as exc:
            self._respond(400, {"error": str(exc)})
        except Exception as exc:
            self.log_message("broker/database error: %s", type(exc).__name__)
            self._respond(503, {"error": "upstream service unavailable"})


class OC2HTTPServer(ThreadingHTTPServer):
    settings: Settings


def main() -> None:
    settings = Settings.from_environment()
    bind_host = os.getenv("OC2_BIND_HOST", "127.0.0.1")
    server = OC2HTTPServer((bind_host, 8088), Handler)
    server.settings = settings
    server.serve_forever()


if __name__ == "__main__":
    main()
