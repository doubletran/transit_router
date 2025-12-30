CREATE OR REPLACE FUNCTION get_one_transfer_geometry(     
point_1 TEXT,     point_2 TEXT 
) 
RETURNS TABLE(
	t_geom geometry
) 
AS $$ BEGIN     
RETURN QUERY     
WITH r1 AS (         
	SELECT              
	id,             
	geom,             
	st_distance(geom::geography, st_geometryfromtext('POINT(' || point_1 || ')', 4326)) AS dis         
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
	st_distance(geom::geography, st_geometryfromtext('POINT(' || point_2 || ')', 4326)) AS dis
	FROM rutas
	WHERE st_distance(geom::geography, st_geometryfromtext('POINT(' || point_2 || ')', 4326)) <= 500
	AND (degrees(st_angle(st_geometryfromtext('LINESTRING(' || point_1 || ', ' || point_2 || ')', 4326), st_makeline(st_startpoint(rutas.geom), st_endpoint(rutas.geom)))) <= 90
	OR degrees(st_angle(st_makeline(st_startpoint(rutas.geom), st_endpoint(rutas.geom)), st_geometryfromtext('LINESTRING(' || point_1 || ', ' || point_2 || ')', 4326))) <= 90)
	ORDER BY st_distance(geom::geography, st_geometryfromtext('POINT(' || point_1 || ')', 4326)) ASC
)
SELECT 
	st_collect(
		ARRAY[
		st_linesubstring(
			r1.geom,
			LEAST(st_linelocatepoint(r1.geom, st_geometryfromtext('POINT(' || point_1 || ')', 4326)), st_linelocatepoint(r1.geom, st_closestpoint(r1.geom, r2.geom))),
			GREATEST(st_linelocatepoint(r1.geom, st_geometryfromtext('POINT(' || point_1 || ')', 4326)), st_linelocatepoint(r1.geom, st_closestpoint(r1.geom, r2.geom)))
		),
		st_linesubstring(
			r2.geom,
			LEAST(st_linelocatepoint(r2.geom, st_geometryfromtext('POINT(' || point_2 || ')', 4326)), st_linelocatepoint(r2.geom, st_closestpoint(r2.geom, r1.geom))),
			GREATEST(st_linelocatepoint(r2.geom, st_geometryfromtext('POINT(' || point_2 || ')', 4326)), st_linelocatepoint(r2.geom, st_closestpoint(r2.geom, r1.geom)))
		)
		]::geometry[]
	) as geom
FROM r1
CROSS JOIN r2
WHERE st_distance(r1.geom::geography, r2.geom::geography) <= 500; 
END; 
$$ LANGUAGE plpgsql