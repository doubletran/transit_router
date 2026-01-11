
import psycopg
import os
from psycopg.rows import dict_row


from dotenv import load_dotenv
import os

# Configuración de la conexión a la base de datos PostgreSQL
load_dotenv()
db_name =os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")



def connectgtfsDb(method="psycopg"):
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
          dbname="sfo_gtfs",
          user=os.getenv("DB_USER"),
          password=os.getenv("DB_PASSWORD"), row_factory=dict_row
      )
    return conn
