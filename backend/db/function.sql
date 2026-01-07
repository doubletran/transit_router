CREATE OR REPLACE FUNCTION public.get_trip_shape_segment(
    p_src_stop_id  TEXT,
    p_dest_stop_id TEXT
)
RETURNS TABLE (
    trip_id  TEXT,
    route_id TEXT,
    shape_id TEXT,
    geom     geometry(LineString, 4326),
    geojson  jsonb
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_trip_id  TEXT;
    v_route_id TEXT;
    v_shape_id TEXT;

    v_line geometry(LineString, 4326);
    v_src  geometry(Point, 4326);
    v_dest geometry(Point, 4326);

    v_f1 double precision;
    v_f2 double precision;
BEGIN
    -------------------------------------------------------------------
    -- 1) Pick ONE best trip that contains src and dest (src before dest)
    --    "Best" here = smallest stop_sequence gap (closest match)
    -------------------------------------------------------------------
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

    IF v_trip_id IS NULL THEN
        RAISE EXCEPTION
          'No trip found where src stop % occurs before dest stop %',
          p_src_stop_id, p_dest_stop_id;
    END IF;

    -------------------------------------------------------------------
    -- 2) Build the full shape line for that trip (shape_id)
    -------------------------------------------------------------------
    SELECT ST_MakeLine(
               ST_SetSRID(ST_MakePoint(s.shape_pt_lon, s.shape_pt_lat), 4326)
               ORDER BY s.shape_pt_sequence
           )
      INTO v_line
    FROM shapes s
    WHERE s.shape_id = v_shape_id;

    IF v_line IS NULL THEN
        RAISE EXCEPTION 'No shape points found for shape_id %', v_shape_id;
    END IF;

    -------------------------------------------------------------------
    -- 3) Get source/destination stop points (lon/lat) from stops table
    -------------------------------------------------------------------
    SELECT ST_SetSRID(ST_MakePoint(stop_lon, stop_lat), 4326)
      INTO v_src
    FROM stops
    WHERE stop_id = p_src_stop_id;

    SELECT ST_SetSRID(ST_MakePoint(stop_lon, stop_lat), 4326)
      INTO v_dest
    FROM stops
    WHERE stop_id = p_dest_stop_id;

    IF v_src IS NULL OR v_dest IS NULL THEN
        RAISE EXCEPTION
          'Stop not found. src=% dest=%',
          p_src_stop_id, p_dest_stop_id;
    END IF;

    -------------------------------------------------------------------
    -- 4) Locate stops along the shape, then cut substring between them
    -------------------------------------------------------------------
    v_f1 := ST_LineLocatePoint(v_line, v_src);
    v_f2 := ST_LineLocatePoint(v_line, v_dest);

    geom := ST_LineSubstring(v_line, LEAST(v_f1, v_f2), GREATEST(v_f1, v_f2));

    trip_id  := v_trip_id;
    route_id := v_route_id;
    shape_id := v_shape_id;
    geojson  := ST_AsGeoJSON(geom)::jsonb;

    RETURN NEXT;
END;
$$;
