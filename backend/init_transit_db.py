import osmnx as ox
import geopandas as gpd
import pandas as pd
from sqlalchemy import create_engine, text

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

  route_path = "data/California_Transit_Routes.geojson"
  stop_path = "data/California_Transit_Stops.geojson"
  route_gdf = gpd.read_file(route_path)
  
  route_gdf.to_postgis(name='route',con=engine, if_exists="replace")
  stop_gdf = gpd.read_file(stop_path)
  stop_gdf.to_postgis(name="stop", con=engine,if_exists="replace")
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
read_sfo_transit()