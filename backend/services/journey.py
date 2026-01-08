from routing.main import compute_raptor
import pandas as pd
from services.stop import *
import services.route as Route
from flask import jsonify
from db import connectDb, connectgtfsDb
TEST_JOURNEY = [('walking', 2948, 2038.0, pd.Timedelta('0 days 00:01:22.800000'), pd.Timestamp('2025-08-30 05:42:22.800000')),(pd.Timestamp('2025-08-30 05:53:14'), 2038, 71, pd.Timestamp('2025-08-30 06:16:41'), '1133_0'),(pd.Timestamp('2025-08-30 06:31:14'), 71, 83, pd.Timestamp('2025-08-30 06:45:18'), '1163_5'),('walking', 83, 1.0, pd.Timedelta('0 days 00:00:19.200000'), pd.Timestamp('2025-08-30 06:45:37.200000'))]
                 

def getJourney(src, dest, dtime):
  srcStop= getReducedStopId(src)
  destStop = getReducedStopId(dest)
  #journey = compute_raptor(srcStop, destStop, dtime)
  journey = TEST_JOURNEY
  routes = []
  stops = []

  #journeyList = []

  srcStop = getOrigStopId(journey[0][1])
  srcStopData = getStop(str(srcStop))
  stopGeojson= {'type': 'Feature',
                  'properties': {'id':srcStopData["stop_id"], 'name': srcStopData["stop_name"]},
                  'geometry': srcStopData["geojson"]}
  stops.append(stopGeojson)
  for leg in journey:
    print(leg)
    #step = [leg[0], leg[1], leg[2]]
    destStop = getOrigStopId(leg[2])
    destStopData = getStop(str(destStop))
    stopGeojson= {'type': 'Feature',
                     'properties': {'id':destStopData["stop_id"], 'name': destStopData["stop_name"]},
                     'geometry': destStopData["geojson"]}
    if leg[0] != "walking":
      trip = Route.getTripSegment(str(srcStop), str(destStop))
      print(trip)
      routeId =trip["route_id"]
      routeColor = Route.getRouteColor(routeId)
      routeGeojson= {'type': 'Feature',
                     'properties': {'color': f'#{routeColor}'},
                     'geometry': trip["geojson"]}
    else:
      print(srcStopData["geojson"]["coordinates"])
      routeGeojson={'type': 'Feature',
                    'geometry': {'type': 'LineString',
                                 'dashArray': "5, 8",
                                 'coordinates':[srcStopData["geojson"]["coordinates"],
                                               destStopData["geojson"]["coordinates"]] }}
      
    stops.append(stopGeojson)
    routes.append(routeGeojson)
    srcStop=destStop
    srcStopData = destStopData
      

  return routes, stops
#print(getJourney(913,3016, 0 ))