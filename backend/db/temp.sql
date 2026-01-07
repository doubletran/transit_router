
--SELECT shape_id, shape_pt_sequence FROM shapes WHERE shape_id IN (SELECT shape_id FROM stop_times st JOIN trips t ON st.trip_id=t.trip_id WHERE route_id='NBUS' GROUP BY shape_id) ORDER BY ST_MakePoint(shape_pt_lon, shape_pt_lat) <-> (SELECT ST_MakePoint(stop_lon, stop_lat) FROM stops WHERE stop_id='4943') LIMIT 1
SELECT t.trip_id, t.route_id, t.shape_id
  INTO v_trip_id, v_route_id, v_shape_id
FROM trips t
JOIN stop_times st_src
  ON st_src.trip_id = t.trip_id
  AND st_src.stop_id = p_src_stop_id
JOIN stop_times st_dest
  ON st_dest.trip_id = t.trip_id
  AND st_dest.stop_id = p_dest_stop_id
WHERE st_src.stop_sequence < st_dest.stop_sequence
ORDER BY (st_dest.stop_sequence - st_src.stop_sequence) ASC
LIMIT 1;
