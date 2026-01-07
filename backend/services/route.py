from routing.main import compute_raptor
import pandas as pd
from services.stop import *
from flask import jsonify
from db import connectDb
def get_route_by_trip(tripId):
    conn = connectDb()
    #point_2 = request.args.get('point_2')
    cursor = conn.cursor()
    cursor.execute("""SELECT route_id FROM trip_mapping WHERE trip_id=%s""", (tripId,))
    data = cursor.fetchone()
    if data is None:
      raise LookupError
    id = data[0]
    return id

def getGeometry(routeId):
    conn = connectDb()
    cursor = conn.cursor()
    cursor.execute("""SELECT jsonb_build_object(
                          'type','Feature',
                          'geometry',ST_AsGeoJSON(geometry)::jsonb) FROM route WHERE route_id=%s""", (routeId, ))
    data = cursor.fetchone()
    if data is None:
      raise LookupError
    #print(data)
    return data[0]
    
def getOrigRouteIdByReducedTripId(reducedTripId):
    conn = connectDb()
    #point_2 = request.args.get('point_2')
    cursor = conn.cursor()
    cursor.execute("""SELECT route_id FROM trip t JOIN trip_mapping m ON m.GTFS_name=t.trip_id WHERE m.new_trip_id=%s""",(reducedTripId,))
    data = cursor.fetchone()
    if data is None:
      raise LookupError
    print("Found Original RouteId: " + data[0])
    return data[0]

  
def get_optimal_route(src, dest, dtime):
  srcStop= getReducedStopId(src)
  destStop = getReducedStopId(dest)
  trips, _, journey = compute_raptor(srcStop, destStop, dtime)
  routes = []

  journeyList = []
  for leg in journey:
    print(leg)
    step = [leg[0], leg[1], leg[2]]
    if leg[0] != "walking":
      routeId = getOrigRouteIdByReducedTripId(leg[4])
      srcStop = getOrigStopId(leg[1])
      destStop = getOrigStopId(leg[2])
      fullRoute = getGeometry(routeId)
      srcLocation = getLocation(str(srcStop))
      destLocation = getLocation(str(destStop))
      min_x= min(srcLocation[0], destLocation[0])
      max_x = max(srcLocation[0], destLocation[0])
      min_y = min(srcLocation[1], destLocation[1])
      max_y = max(srcLocation[1], destLocation[1])
      print(min_x, max_x, min_y, max_y)
      filteredCoords = []
      for coord in fullRoute['geometry']['coordinates']:
        print(coord)
        if min_x < coord[0] < max_x and min_y < coord[1] < max_y:
          filteredCoords.append(coord)
      print(filteredCoords)
      
      #fullRoute['geometry']['coordinates'] = filteredCoords
        
      routes.append(fullRoute)
  
      
    #leg = ('walking', src, dst, time, arival time)
    reducedStopId = leg[1]
    step[1] = getOrigStopId(int(reducedStopId))
    reducedStopId = leg[2]
    step[2] = getOrigStopId(int(reducedStopId))
    #step[3] = step[3].total_seconds()
    #step[4] = step[4].time()
    journeyList.append(step)

  return journeyList, routes
    
    
    

#get_optimal_route(913, 3016,pd.to_datetime('2025-08-30 05:41:00') )
#getOrigRouteByReducedTripId("1133_5")
  
  