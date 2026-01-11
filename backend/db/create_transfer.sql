DROP TABLE IF EXISTS transfers;
CREATE TABLE transfers (
  src_stop_id TEXT NOT NULL,
  dest_stop_id TEXT NOT NULL,
  min_transfer_time INTEGER,
  path geometry(LineString, 4326)
);

-- optional: prevent duplicates
CREATE UNIQUE INDEX IF NOT EXISTS transfer_pair
ON transfers (LEAST(src_stop_id, dest_stop_id), GREATEST(src_stop_id, dest_stop_id))