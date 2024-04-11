from flask import Flask, jsonify
import psycopg2
from shapely.wkb import loads

app = Flask(__name__)

# PostGIS database connection details
dbname = 'gis5572'
user = 'postgres'
password = 'Hyderabad43%'
host = '35.238.64.215'  # Cloud DB Public IP address
port = '5432'

@app.route('/get_polygon', methods=['GET'])
def get_polygon():
    # Connect to the PostGIS database
    connection = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
    cursor = connection.cursor()
    # Replace name of the table with the actual table name
    table_name = ' ebk_points'
    # Execute SQL query to retrieve the geometry data
    sql_query = f"SELECT shape FROM {table_name};"
    cursor.execute(sql_query)
    # Fetch all the results
    rows = cursor.fetchall()
    # Close database connection
    cursor.close()
    connection.close()
    # Convert the geometry data to GeoJSON format
    features = []
    for row in rows:
        try:
            # Convert WKB geometry to GeoJSON
            geojson = wkb_to_geojson(row[0])
            features.append({"type": "Feature", "geometry": geojson})
        except Exception as e:
            print(f"Error converting geometry: {e}")
    # Return the GeoJSON data as a FeatureCollection
    return jsonify({"type": "FeatureCollection", "features": features})
def wkb_to_geojson(wkb):
    # Convert WKB to GeoJSON
    geometry = loads(wkb, hex=True)
    return geometry.__geo_interface__
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
