CREATE OR REPLACE FUNCTION get_two_transfer_routes_geojson(     
    point_1 TEXT,     
    point_2 TEXT 
) 
RETURNS SETOF json
AS $$ 
BEGIN     
    RETURN QUERY     
    WITH r1 AS (         
        SELECT              
            id,             
            geom,
            "Ruta",
            "Tipo_de_Transporte",
            "Clase_de_Servicio"
        FROM rutas         
        WHERE st_distance(geom::geography, st_geometryfromtext('POINT(' || point_1 || ')', 4326)) <= 500         
        AND (degrees(st_angle(st_geometryfromtext('LINESTRING(' || point_1 || ', ' || point_2 || ')', 4326), st_makeline(st_startpoint(rutas.geom), st_endpoint(rutas.geom)))) <= 90         
        OR degrees(st_angle(st_makeline(st_startpoint(rutas.geom), st_endpoint(rutas.geom)), st_geometryfromtext('LINESTRING(' || point_1 || ', ' || point_2 || ')', 4326))) <= 90)         
        ORDER BY st_distance(geom::geography, st_geometryfromtext('POINT(' || point_1 || ')', 4326)) ASC
    ),     
    r2 AS (         
        SELECT              
            id,             
            geom,
            "Ruta",
            "Tipo_de_Transporte",
            "Clase_de_Servicio"
        FROM rutas
        WHERE st_distance(geom::geography, st_geometryfromtext('POINT(' || point_2 || ')', 4326)) <= 500
        AND (degrees(st_angle(st_geometryfromtext('LINESTRING(' || point_1 || ', ' || point_2 || ')', 4326), st_makeline(st_startpoint(rutas.geom), st_endpoint(rutas.geom)))) <= 90
        OR degrees(st_angle(st_makeline(st_startpoint(rutas.geom), st_endpoint(rutas.geom)), st_geometryfromtext('LINESTRING(' || point_1 || ', ' || point_2 || ')', 4326))) <= 90)
        ORDER BY st_distance(geom::geography, st_geometryfromtext('POINT(' || point_2 || ')', 4326)) ASC
    ),
    r3 AS (
        SELECT
            r.id,
            r.geom,
            r."Ruta",
            r."Tipo_de_Transporte",
            r."Clase_de_Servicio"
        FROM rutas r
        WHERE r.id NOT IN (
            SELECT id FROM r1 UNION SELECT id from r2
        )
        AND (degrees(st_angle(st_geometryfromtext('LINESTRING(' || point_1 || ', ' || point_2 || ')', 4326), st_makeline(st_startpoint(r.geom), st_endpoint(r.geom)))) <= 90
        OR degrees(st_angle(st_makeline(st_startpoint(r.geom), st_endpoint(r.geom)), st_geometryfromtext('LINESTRING(' || point_1 || ', ' || point_2 || ')', 4326))) <= 90)
        ORDER BY st_distance(geom::geography, st_geometryfromtext('POINT(' || point_2 || ')', 4326)) ASC
    )
    SELECT 
        json_build_object(
            'type', 'Feature',
            'geometry', json_build_object(
                'type', 'MultiLineString',
                'coordinates', json_build_array(
                    st_asgeojson(
                        st_linesubstring(
                            r1.geom,
                            LEAST(st_linelocatepoint(r1.geom, st_geometryfromtext('POINT(' || point_1 || ')', 4326)), st_linelocatepoint(r1.geom, st_closestpoint(r1.geom, r3.geom))),
                            GREATEST(st_linelocatepoint(r1.geom, st_geometryfromtext('POINT(' || point_1 || ')', 4326)), st_linelocatepoint(r1.geom, st_closestpoint(r1.geom, r3.geom)))
                        )
                    )::json->'coordinates',
                    st_asgeojson(
                        st_linesubstring(
                            r3.geom,
                            LEAST(st_linelocatepoint(r3.geom, st_closestpoint(r3.geom, r1.geom)), st_linelocatepoint(r3.geom, st_closestpoint(r3.geom, r2.geom))),
                            GREATEST(st_linelocatepoint(r3.geom, st_closestpoint(r3.geom, r1.geom)), st_linelocatepoint(r3.geom, st_closestpoint(r3.geom, r2.geom)))
                        )
                    )::json->'coordinates',
                    st_asgeojson(
                        st_linesubstring(
                            r2.geom,
                            LEAST(st_linelocatepoint(r2.geom, st_geometryfromtext('POINT(' || point_2 || ')', 4326)), st_linelocatepoint(r2.geom, st_closestpoint(r2.geom, r3.geom))),
                            GREATEST(st_linelocatepoint(r2.geom, st_geometryfromtext('POINT(' || point_2 || ')', 4326)), st_linelocatepoint(r2.geom, st_closestpoint(r2.geom, r3.geom)))
                        )
                    )::json->'coordinates'
                )
            ),
            'properties', json_build_object(
                'bus_number', 3,
                'route_1', r1."Ruta",
                'route_1_type', r1."Tipo_de_Transporte",
                'route_1_class', r1."Clase_de_Servicio",
                'route_2', r3."Ruta",
                'route_2_type', r3."Tipo_de_Transporte",
                'route_2_class', r3."Clase_de_Servicio",
                'route_3', r2."Ruta",
                'route_3_type', r2."Tipo_de_Transporte",
                'route_3_class', r2."Clase_de_Servicio"
            )
        )
    FROM r1
    CROSS JOIN r3
    CROSS JOIN r2
    WHERE st_distance(r3.geom::geography, r1.geom::geography) <= 500 
    AND st_distance(r3.geom::geography, r2.geom::geography) <= 500
	ORDER BY (st_length(st_linesubstring(
						r1.geom,
						LEAST(st_linelocatepoint(r1.geom, st_geometryfromtext('POINT(' || point_1 || ')', 4326)), st_linelocatepoint(r1.geom, st_closestpoint(r1.geom, r3.geom))),
						GREATEST(st_linelocatepoint(r1.geom, st_geometryfromtext('POINT(' || point_1 || ')', 4326)), st_linelocatepoint(r1.geom, st_closestpoint(r1.geom, r3.geom)))
					)) +
		   st_length(st_linesubstring(
						r3.geom,
						LEAST(st_linelocatepoint(r3.geom, st_closestpoint(r3.geom, r1.geom)), st_linelocatepoint(r3.geom, st_closestpoint(r3.geom, r2.geom))),
						GREATEST(st_linelocatepoint(r3.geom, st_closestpoint(r3.geom, r1.geom)), st_linelocatepoint(r3.geom, st_closestpoint(r3.geom, r2.geom)))
					)) +
		   st_length(st_linesubstring(
						r2.geom,
						LEAST(st_linelocatepoint(r2.geom, st_geometryfromtext('POINT(' || point_2 || ')', 4326)), st_linelocatepoint(r2.geom, st_closestpoint(r2.geom, r3.geom))),
						GREATEST(st_linelocatepoint(r2.geom, st_geometryfromtext('POINT(' || point_2 || ')', 4326)), st_linelocatepoint(r2.geom, st_closestpoint(r2.geom, r3.geom)))
					))
		  ) ASC limit 15;
END; 
$$ LANGUAGE plpgsql;
