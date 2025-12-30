CREATE OR REPLACE FUNCTION get_one_transfer_routes_geojson(     
point_1 TEXT,     point_2 TEXT 
) 
RETURNS SETOF json
AS $$ BEGIN     
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
	ORDER BY st_distance(geom::geography, st_geometryfromtext('POINT(' || point_1 || ')', 4326)) ASC
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
						LEAST(st_linelocatepoint(r1.geom, st_geometryfromtext('POINT(' || point_1 || ')', 4326)), st_linelocatepoint(r1.geom, st_closestpoint(r1.geom, r2.geom))),
						GREATEST(st_linelocatepoint(r1.geom, st_geometryfromtext('POINT(' || point_1 || ')', 4326)), st_linelocatepoint(r1.geom, st_closestpoint(r1.geom, r2.geom)))
					)
				)::json->'coordinates',
				st_asgeojson(
					st_linesubstring(
						r2.geom,
						LEAST(st_linelocatepoint(r2.geom, st_geometryfromtext('POINT(' || point_2 || ')', 4326)), st_linelocatepoint(r2.geom, st_closestpoint(r2.geom, r1.geom))),
						GREATEST(st_linelocatepoint(r2.geom, st_geometryfromtext('POINT(' || point_2 || ')', 4326)), st_linelocatepoint(r2.geom, st_closestpoint(r2.geom, r1.geom)))
					)
				)::json->'coordinates'
			)
		),
		'properties', json_build_object(
			'bus_number', 2,
			'route_1', r1."Ruta",
			'route_1_type', r1."Tipo_de_Transporte",
			'route_1_class', r1."Clase_de_Servicio",
			'route_2', r2."Ruta",
			'route_2_type', r2."Tipo_de_Transporte",
			'route_2_class', r2."Clase_de_Servicio"
		)
	)
FROM r1
CROSS JOIN r2
WHERE st_distance(r1.geom::geography, r2.geom::geography) <= 500
ORDER BY (
	st_length(
			st_linesubstring(
			r1.geom,
			LEAST(st_linelocatepoint(r1.geom, st_geometryfromtext('POINT(' || point_1 || ')', 4326)), st_linelocatepoint(r1.geom, st_closestpoint(r1.geom, r2.geom))),
			GREATEST(st_linelocatepoint(r1.geom, st_geometryfromtext('POINT(' || point_1 || ')', 4326)), st_linelocatepoint(r1.geom, st_closestpoint(r1.geom, r2.geom))))
	)
	+ 
	st_linesubstring(
		r2.geom,
		LEAST(st_linelocatepoint(r2.geom, st_geometryfromtext('POINT(' || point_2 || ')', 4326)), st_linelocatepoint(r2.geom, st_closestpoint(r2.geom, r1.geom))),
		GREATEST(st_linelocatepoint(r2.geom, st_geometryfromtext('POINT(' || point_2 || ')', 4326)), st_linelocatepoint(r2.geom, st_closestpoint(r2.geom, r1.geom)))
	)
)
LIMIT 15; 
END; 
$$ LANGUAGE plpgsql