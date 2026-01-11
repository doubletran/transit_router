import psycopg, json
from db import connectgtfsDb

def updateTransfers(transfers):
  
  sql = """
  INSERT INTO transfers (src_stop_id, dest_stop_id, min_transfer_time, path)
  VALUES (%s, %s, %s, ST_GeomFromGeoJSON(%s::jsonb))
  ON CONFLICT (
    LEAST(src_stop_id, dest_stop_id),
    GREATEST(src_stop_id, dest_stop_id)
  )
  DO UPDATE SET
    min_transfer_time = EXCLUDED.min_transfer_time,
    path = EXCLUDED.path;
  """
  conn = connectgtfsDb()
  with conn.cursor() as cur:

      rows = [
          (r.src_stop_id, r.dest_stop_id, int(r.min_transfer_time), json.dumps({'type': 'LineString', 'coordinates': r.path}))
          for r in transfers.itertuples(index=False)
      ]
      #print(rows)
      cur.executemany(sql, rows)
  conn.commit()   
  conn.close()
  
def getTransfer(stop1, stop2):
  srcStopId = str(min(stop1, stop2))
  destStopId=str(max(stop1, stop2))
  print(srcStopId, destStopId)
  conn = connectgtfsDb()
  cursor = conn.cursor()
  cursor.execute("""SELECT ST_AsGeoJSON(path) as geojson, min_transfer_time FROM transfers WHERE src_stop_id=%s AND dest_stop_id=%s""",(srcStopId,destStopId))
  data = cursor.fetchone()
  if data is None:
      raise LookupError
  return data

  