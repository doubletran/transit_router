from connect import get_db_connection

def getNearestStop(lat: float, lon: float)->int:
    conn = get_db_connection()
    #point_2 = request.args.get('point_2')
    cursor = conn.cursor()
    cursor.execute("""SELECT id, stop_name FROM stop ORDER BY geometry <-> ST_SetSRID(ST_MakePoint(%s,%s),4326) LIMIT 1;""", (lon, lat))
    data = cursor.fetchone()
    if data is None:
      raise LookupError
    id, name = data
    return id
  
#getNearestStop(37.772618,-122.38978)