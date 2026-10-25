CREATE EXTENSION IF NOT EXISTS timescaledb;
CREATE TABLE IF NOT EXISTS oc2_events (
 event_id UUID NOT NULL,
 event_time TIMESTAMPTZ NOT NULL,
 ingested_at TIMESTAMPTZ NOT NULL DEFAULT now(),
 source_id TEXT NOT NULL,
 mode TEXT NOT NULL CHECK(mode IN ('simulation','live')),
 event_type TEXT NOT NULL,
 schema_version TEXT NOT NULL,
 bearing_deg DOUBLE PRECISION,
 confidence DOUBLE PRECISION CHECK(confidence IS NULL OR confidence BETWEEN 0 AND 1),
 payload JSONB NOT NULL,
 PRIMARY KEY (event_time,event_id)
);
SELECT create_hypertable('oc2_events','event_time',if_not_exists=>TRUE);
CREATE INDEX IF NOT EXISTS idx_oc2_source_time ON oc2_events(source_id,event_time DESC);
CREATE INDEX IF NOT EXISTS idx_oc2_kind_time ON oc2_events(event_type,event_time DESC);
CREATE TABLE IF NOT EXISTS oc2_tracks (
 track_id TEXT PRIMARY KEY, source_id TEXT NOT NULL, mode TEXT NOT NULL,
 created_at TIMESTAMPTZ NOT NULL DEFAULT now(), metadata JSONB NOT NULL DEFAULT '{}'::jsonb
);
INSERT INTO oc2_tracks(track_id,source_id,mode,metadata) VALUES
 ('sim-track-001','oc2-sim','simulation','{"class":"synthetic-object","seed":2026}'::jsonb),
 ('sim-track-002','oc2-sim','simulation','{"class":"synthetic-object","seed":2027}'::jsonb)
ON CONFLICT (track_id) DO NOTHING;
