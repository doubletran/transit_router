from routing.main import compute_raptor
import pandas as pd
from stop import *
from db.connect import get_db_connection
def get_route_by_trip(tripId):
    conn = get_db_connection()
    #point_2 = request.args.get('point_2')
    cursor = conn.cursor()
    cursor.execute("""SELECT route_id FROM trip_mapping WHERE trip_id=%s""", (tripId,))
    data = cursor.fetchone()
    if data is None:
      raise LookupError
    id = data[0]
    return id

def get_optimal_route(src, dest, dtime):
  srcStop= getReducedStopId(src)
  destStop = getReducedStopId(dest)
  trips, _, journey = compute_raptor(srcStop, destStop, dtime)
  routes = []
  print(trips)
  for tripId in trips:
    routes.append(tripId.split("_")[0])
  print(journey)
  journeyList = []
  for leg in journey:
    step = list(leg)
    #leg = ('walking', src, dst, time, arival time)
    reducedStopId = leg[1]
    step[1] = getOrigStopId(int(reducedStopId))
    reducedStopId = leg[2]
    step[2] = getOrigStopId(int(reducedStopId))
    journeyList.append(step)
    
  return journeyList
    
    
    

get_optimal_route(913, 3016,pd.to_datetime('2025-08-30 05:41:00') )
  
  