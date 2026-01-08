ALTER TABLE stops
ALTER COLUMN stop_geom
TYPE geometry(Point, 4326)
USING ST_Transform(stop_geom, 4326);
