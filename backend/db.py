import osmnx as ox
import geopandas as gpd
import pandas as pd
from sqlalchemy import create_engine, text
from geoalchemy2 import Geometry
from routing.config import DATA_PATH
import psycopg
import os

from dotenv import load_dotenv
import os

# Configuración de la conexión a la base de datos PostgreSQL
load_dotenv()
db_name =os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")



def connectDb(method="psycopg"):
    """
    Establish a connection to the PostgreSQL database using psycopg.
    Database connection parameters are retrieved from environment variables.

    Returns:
        psycopg.Connection: Connection object for interacting with the PostgreSQL database.
    """
    if method=="psycopg":
      conn = psycopg.connect(
          host=os.getenv("DB_HOST"),
          port=os.getenv("DB_PORT"),
          dbname=os.getenv("DB_NAME"),
          user=os.getenv("DB_USER"),
          password=os.getenv("DB_PASSWORD")
      )
    else:
      conn = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
    return conn


def read_california_transit():
  engine = connectDb("sql")
  route_path = "SFO_Routes.geojson"
  stop_path = "SFO_Stops.geojson"
  route_gdf = gpd.read_file(route_path)
  route_gdf = route_gdf.to_crs(4326)

  route_gdf.to_postgis(name='route',con=engine, if_exists="replace", dtype={"geometry": Geometry("LINESTRING", srid=4326)} )
  stop_gdf = gpd.read_file(stop_path)
  stop_gdf = stop_gdf.to_crs(4326)
  stop_gdf.to_postgis(name="stop", con=engine,if_exists="replace", dtype={"geom": Geometry("POINT",srid=4326 )})
def read_sfo_transit():
  conn = connectDb("sql")
  stops_df = pd.read_csv("data/sfo_gtfs/stops.txt")
  stops_df.to_sql(
    name="sfo_stop",
    con=conn,
    if_exists="replace",   # 'replace' to recreate table
    index=False)
  route_df = pd.read_csv("data/sfo_gtfs/routes.txt")
  route_df.to_sql(
    name="sfo_route",
    con=conn,
    if_exists="replace",   # 'replace' to recreate table
    index=False)

def read_mapping():
  trip_df = pd.read_csv(os.path.join(DATA_PATH,"gtfs_o","trips.txt"))
  engine=connectDb("sql")
  trip_df.to_sql(    
    name="trip",
    con=engine,
    if_exists="replace",
    index=False
  )
  stops_df = pd.read_csv(os.path.join(DATA_PATH,"trip_mappings.csv"))
  stops_df.rename(columns={"GTFS_name": "gtfs_name"}, inplace=True)
  stops_df["gtfs_name"] = stops_df['gtfs_name'].astype(str)
  stops_df.to_sql(
    name="trip_mapping",
    con=engine,
    if_exists="replace",
    index=False
  )
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
#read_california_transit()
read_mapping()
print(DATA_PATH)