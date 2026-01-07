INSERT INTO shape_geoms
SELECT shape_id, ST_MakeLine(array_agg(
  ST_Transform(ST_Point(shape_pt_lon, shape_pt_lat, 4326), 3857) ORDER BY shape_pt_sequence))
FROM shapes
GROUP BY shape_id;

UPDATE stops
SET stop_geom = ST_Transform(ST_Point(stop_lon, stop_lat, 4326), 3857);
			