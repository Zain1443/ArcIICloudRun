from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

# PostGIS database connection details
dbname = 'lab1'
user = 'postgres'
password = 'Hyderabad43%'
host = '34.122.229.143'  # Update to your SQL Database external IP
port = '5432'

@app.route('/get_polygon', methods=['GET'])
def get_polygon():
    # Connect to the PostGIS database
    connection = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
    cursor = connection.cursor()

    # Replace 'your_table' with the actual table name
    table_name = 'Zain_Table'

    # Execute SQL query to retrieve the polygon as GeoJSON
    sql_query = f"SELECT ST_AsGeoJSON(geom) FROM {table_name};"
    cursor.execute(sql_query)

    # Fetch the result
    geojson = cursor.fetchone()[0]

    # Close database connection
    cursor.close()
    connection.close()

    return jsonify({"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": geojson}]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
