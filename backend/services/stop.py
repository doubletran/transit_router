from db import connectDb, connectgtfsDb

def getNearestStop(lat: float, lon: float)->int:
    conn = connectDb()
    #point_2 = request.args.get('point_2')
    cursor = conn.cursor()
    cursor.execute("""SELECT id, stop_name FROM stop ORDER BY geometry <-> ST_SetSRID(ST_MakePoint(%s,%s),4326) LIMIT 1;""", (lon, lat))
    data = cursor.fetchone()
    if data is None:
      raise LookupError
    id, name = data
    return id
def getStop(id):
  conn = connectgtfsDb()
  cursor = conn.cursor()
  cursor.execute("""SELECT stop_id, stop_name, ST_AsGeoJSON(stop_geom)::jsonb as geojson FROM stops WHERE stop_id=%s;""", (id,))
  data = cursor.fetchone()
  if data is None:
    raise LookupError
  conn.close()
  return data
def getLocation(stopId):
  conn = connectDb()
  cursor = conn.cursor()
  cursor.execute("""SELECT ST_X(geometry), ST_Y(geometry) FROM stop WHERE stop_id=%s;""", (stopId,))
  data = cursor.fetchone()
  if data is None:
    raise LookupError
  print(data)
  conn.close()
  return [data[0], data[1]]
def getReducedStopId(stopId:int) -> int:
  conn  = connectDb()
  cursor = conn.cursor()
  cursor.execute("""SELECT new_stop_id FROM sfo_stop_mapping WHERE stop_id=%s;""",(stopId,))
  data = cursor.fetchone()
  if data is None:
    raise LookupError
  id = data[0]
  conn.close()
  print(id)
  return id
def getOrigStopId(reducedStopId:int) -> int:
  conn  = connectDb()
  cursor = conn.cursor()
  cursor.execute("""SELECT stop_id FROM sfo_stop_mapping WHERE new_stop_id=%s;""",(reducedStopId,))
  data = cursor.fetchone()
  if data is None:
    raise LookupError
  id = data[0]
  conn.close()
  print(id)
  return id
#getNearestStop(37.772618,-122.38978)
#getMappedStop(3018)
#getLocation('6083')
#print(getStop('6083'))