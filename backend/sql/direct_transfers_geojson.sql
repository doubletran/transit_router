CREATE OR REPLACE FUNCTION get_direct_routes_geojson(     
start_point TEXT,     end_point TEXT 
) 
RETURNS SETOF json
AS $$ BEGIN     
RETURN QUERY     
SELECT 
	json_build_object(
		'type', 'Feature',
        'geometry', json_build_object(
			'type', 'MultiLineString',
			'coordinates', st_asgeojson(st_linesubstring(f.geom,
				least(st_linelocatepoint(f.geom, st_geometryfromtext('POINT(' || start_point || ')', 4326)), st_linelocatepoint(f.geom, st_geometryfromtext('POINT(' || end_point || ')', 4326))),
				greatest(st_linelocatepoint(f.geom, st_geometryfromtext('POINT(' || start_point || ')', 4326)), st_linelocatepoint(f.geom, st_geometryfromtext('POINT(' || end_point || ')', 4326)))
			))::json->'coordinates'
		),
		'properties', json_build_object(
			'bus_number', 1,
			'route', f."ruta",
			'route_type', f."tipo_de_transporte",
			'route_class', f."clase_de_servicio"
		)
	)
FROM get_filtered_direct_routes(start_point, end_point) f
ORDER BY (
	st_length(st_linesubstring(f.geom,
				least(st_linelocatepoint(f.geom, st_geometryfromtext('POINT(' || start_point || ')', 4326)), st_linelocatepoint(f.geom, st_geometryfromtext('POINT(' || end_point || ')', 4326))),
				greatest(st_linelocatepoint(f.geom, st_geometryfromtext('POINT(' || start_point || ')', 4326)), st_linelocatepoint(f.geom, st_geometryfromtext('POINT(' || end_point || ')', 4326)))
			))
)
limit 15;
END; 
$$ LANGUAGE plpgsql