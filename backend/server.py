from flask import Flask, jsonify, request
from flask_cors import CORS
import services.stop as StopService
import services.route as RouteService
import services.journey as Journey
from dotenv import load_dotenv
import os
import psycopg
import pandas as pd

# Load environment variables from a .env file
load_dotenv()

# Initialize a Flask application
app = Flask(__name__)

# Enable Cross-Origin Resource Sharing (CORS) for the Flask application
CORS(app)

def get_db_connection():
    """
    Establish a connection to the PostgreSQL database using psycopg.
    Database connection parameters are retrieved from environment variables.

    Returns:
        psycopg.Connection: Connection object for interacting with the PostgreSQL database.
    """
    conn = psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    return conn
@app.route('/stops', methods=['GET'])
def getAllStops():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT json_agg(
        json_build_object(
            'id', id,
            'name', stop_name,
            'lat', ST_Y(geometry),
            'lng', ST_X(geometry)
        )
    )
    FROM stop;
""")
    data = cursor.fetchall()
    print(data)
    conn.close()
    return data
@app.route('/stop', methods=['GET'])
def getNearestStop():
    conn = get_db_connection()
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    
    if not lat or not lon:
        return jsonify({"error": "lat and lon required"}), 400

    lat = float(lat)
    lon = float(lon)
    #point_2 = request.args.get('point_2')
    cursor = conn.cursor()
    cursor.execute("""SELECT json_build_object('id', id, 'name', stop_name) FROM stop ORDER BY geometry <-> ST_SetSRID(ST_MakePoint(%s,%s),4326) LIMIT 1;""", (lon, lat))
    data = cursor.fetchone()
    if data is None:
        return jsonify({"error": "No stop found"})
    return jsonify(data)
@app.route('/journey', methods=['GET'])
def getJourney():
    srclat = request.args.get('fromlat')
    srclon = request.args.get('fromlon')
    destlat = request.args.get('tolat')
    destlon = request.args.get('tolon')
    srcStop = StopService.getNearestStop(srclat, srclon)
    destStop = StopService.getNearestStop(destlat, destlon)
    print(srcStop)
    print(destStop)
    try:
        #journey, geometry= RouteService.get_optimal_route(srcStop,destStop, pd.to_datetime('2025-08-30 05:41:00'))
        routes, stops= Journey.getJourney(913,3016, pd.to_datetime('2025-08-30 05:41:00'))
        res = {"routes":routes , "stops": stops}
        return jsonify(res), 200
    except Exception as e:
        return jsonify(
            error="Internal server error",
            details=str(e)
        ), 500
@app.route('/route/<id>', methods=['GET'])
def getRoute(id):
    try:
        #journey, geometry= RouteService.get_optimal_route(srcStop,destStop, pd.to_datetime('2025-08-30 05:41:00'))
        route = RouteService.getGeometry(id)
        return route, 200
    except Exception as e:
        return jsonify(
            error="Internal server error",
            details=str(e)
        ), 500


if __name__ == '__main__':
    # Run the Flask application in debug mode, accessible on all network interfaces
    app.run(debug=True, host='0.0.0.0', port=5000)
