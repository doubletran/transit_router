WITH r1 AS (         
	SELECT              
	id,             
	geom,
	"Ruta"
	FROM rutas         
	WHERE st_distance(geom::geography, st_geometryfromtext('POINT(-89.1264672 13.7244551)', 4326)) <= 500         
	AND (degrees(st_angle(st_geometryfromtext('LINESTRING(-89.1264672 13.7244551, -89.2376645 13.6917575)', 4326), st_makeline(st_startpoint(rutas.geom), st_endpoint(rutas.geom)))) <= 90         
	OR degrees(st_angle(st_makeline(st_startpoint(rutas.geom), st_endpoint(rutas.geom)), st_geometryfromtext('LINESTRING(-89.1264672 13.7244551, -89.2376645 13.6917575)', 4326))) <= 90)         
	ORDER BY st_distance(geom::geography, st_geometryfromtext('POINT(-89.1264672 13.7244551)', 4326)) ASC
),     
r2 AS (         
	SELECT              
	id,             
	geom,
	"Ruta"
	FROM rutas
	WHERE st_distance(geom::geography, st_geometryfromtext('POINT(-89.2376645 13.6917575)', 4326)) <= 500
	AND (degrees(st_angle(st_geometryfromtext('LINESTRING(-89.1264672 13.7244551, -89.2376645 13.6917575)', 4326), st_makeline(st_startpoint(rutas.geom), st_endpoint(rutas.geom)))) <= 90
	OR degrees(st_angle(st_makeline(st_startpoint(rutas.geom), st_endpoint(rutas.geom)), st_geometryfromtext('LINESTRING(-89.1264672 13.7244551, -89.2376645 13.6917575)', 4326))) <= 90)
	ORDER BY st_distance(geom::geography, st_geometryfromtext('POINT(-89.2376645 13.6917575)', 4326)) ASC
),
r3 AS (
	SELECT
	r.id,
	r.geom,
	r."Ruta"
	FROM rutas r
	WHERE r.id NOT IN (
		SELECT id FROM r1 UNION SELECT id from r2
	)
	AND (degrees(st_angle(st_geometryfromtext('LINESTRING(-89.1264672 13.7244551, -89.2376645 13.6917575)', 4326), st_makeline(st_startpoint(r.geom), st_endpoint(r.geom)))) <= 90
	OR degrees(st_angle(st_makeline(st_startpoint(r.geom), st_endpoint(r.geom)), st_geometryfromtext('LINESTRING(-89.1264672 13.7244551, -89.2376645 13.6917575)', 4326))) <= 90)
	ORDER BY st_distance(geom::geography, st_geometryfromtext('POINT(-89.2376645 13.6917575)', 4326)) ASC
)
select 
	st_linesubstring(
						r1.geom,
						LEAST(st_linelocatepoint(r1.geom, st_geometryfromtext('POINT(-89.1264672 13.7244551)', 4326)), st_linelocatepoint(r1.geom, st_closestpoint(r1.geom, r3.geom))),
						GREATEST(st_linelocatepoint(r1.geom, st_geometryfromtext('POINT(-89.1264672 13.7244551)', 4326)), st_linelocatepoint(r1.geom, st_closestpoint(r1.geom, r3.geom)))
					),
	r1."Ruta",
	
	st_linesubstring(
						r3.geom,
						LEAST(st_linelocatepoint(r3.geom, st_closestpoint(r3.geom, r1.geom)), st_linelocatepoint(r3.geom, st_closestpoint(r3.geom, r2.geom))),
						GREATEST(st_linelocatepoint(r3.geom, st_closestpoint(r3.geom, r1.geom)), st_linelocatepoint(r3.geom, st_closestpoint(r3.geom, r2.geom)))
					),
	r3."Ruta",
	
	st_linesubstring(
						r2.geom,
						LEAST(st_linelocatepoint(r2.geom, st_geometryfromtext('POINT(-89.2376645 13.6917575)', 4326)), st_linelocatepoint(r2.geom, st_closestpoint(r2.geom, r3.geom))),
						GREATEST(st_linelocatepoint(r2.geom, st_geometryfromtext('POINT(-89.2376645 13.6917575)', 4326)), st_linelocatepoint(r2.geom, st_closestpoint(r2.geom, r3.geom)))
					),
	r2."Ruta"
from 
r1 cross join
r3 cross join 
r2
where st_distance(r3.geom::geography, r1.geom::geography) <= 500 and st_distance(r3.geom::geography, r2.geom::geography) <= 500;