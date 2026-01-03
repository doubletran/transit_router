import osmnx as ox
import geopandas as gpd
import pandas as pd
from sqlalchemy import create_engine, text
from geoalchemy2 import Geometry
from routing.config import DATA_PATH
import os
# Configuración de la conexión a la base de datos PostgreSQL
db_name = 'transit_db'
db_user = 'postgres'
db_password = 'doubletran'
db_host = 'localhost'
db_port = '5432'

# Crear la conexión
#engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
def read_california_transit():

  route_path = "SFO_Routes.geojson"
  stop_path = "SFO_Stops.geojson"
  route_gdf = gpd.read_file(route_path)
  route_gdf.to_postgis(name='route',con=engine, if_exists="replace")
  stop_gdf = gpd.read_file(stop_path)
  stop_gdf = stop_gdf.to_crs(4326)
  stop_gdf.to_postgis(name="stop", con=engine,if_exists="replace", dtype={"geom": Geometry("POINT",srid=4326 )})
def read_sfo_transit():
  stops_df = pd.read_csv("data/sfo_gtfs/stops.txt")
  stops_df.to_sql(
    name="sfo_stop",
    con=engine,
    if_exists="replace",   # 'replace' to recreate table
    index=False)
  route_df = pd.read_csv("data/sfo_gtfs/routes.txt")
  route_df.to_sql(
    name="sfo_route",
    con=engine,
    if_exists="replace",   # 'replace' to recreate table
    index=False)
read_california_transit()
def read_mapping():
  stops_df = pd.read_csv(os.path.join(DATA_PATH,"stops_mappings.csv"))
  stops_df.to_sql(
    name="sfo_stop_mapping",
    con=engine,
    if_exists="replace",
    index=False
  )
  route_df = pd.read_csv(os.path.join(DATA_PATH,"route_mappings.csv"))
  route_df.to_sql(
    name="sfo_route_mapping",
    con=engine,
    if_exists="replace",
    index=False
  )
read_mapping()
print(DATA_PATH)