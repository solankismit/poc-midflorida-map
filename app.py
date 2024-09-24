import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson.json_util import dumps
from flask_cors import CORS

import math
from flask import Flask, request, jsonify

app = Flask(__name__)
CORS(app)

client = MongoClient('mongodb+srv://projectssmit:8FvTZSs4pQ7sADQK@midfloridadata.nungw.mongodb.net/?retryWrites=true&w=majority&appName=MidFloridaData') 
# use a database named "myDatabase"
db = client["map-data"]
collection = db["midflorida-data"]

# Get all the data of collection and save all the data in data var
data = list(collection.find({}))




def deg2rad(deg):
    return deg * (math.pi / 180)

def calculate_distance(lat1, lon1, lat2, lon2):
  R = 6371  # Radius of the Earth in kilometers
  dLat = deg2rad(lat2 - lat1)
  dLon = deg2rad(lon2 - lon1)
  a = math.sin(dLat / 2) * math.sin(dLat / 2) + math.cos(deg2rad(lat1)) * math.cos(deg2rad(lat2)) * math.sin(dLon / 2) * math.sin(dLon / 2)
  c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
  distance = R * c  # Distance in kilometers
  distance_in_miles = math.floor(distance / 1.609) 
  return distance_in_miles


@app.route("/")
def hello_world():
  """Example Hello World route."""
  name = os.environ.get("NAME", "World")
  return f"Hello {name}!"


@app.route("/data")
def get_locations():
    lat_str = request.args.get("lat")
    lon_str = request.args.get("lng")
    # Single-line null checks and conversions with error handling
    lat = float(lat_str) if lat_str else None
    lon = float(lon_str) if lon_str else None

    categories_string = request.args.get("categories")
    categories = categories_string.split(",") if categories_string else [] 
    print(categories)
    max_distance = int(request.args.get("distance", 0)) 
    # Fetch data from MongoDB
    query = {}
    if categories:
        query["locationTypeList"] = {"$in": categories}  # Filter by categories
    all_locations = collection.find(query,{'_id': 0})
    filtered_data = []
    if lat is None or lon is None:
      
        return jsonify(list(all_locations))

    for item in all_locations:
        item_lat = item["latitude"]
        item_lon = item["longitude"]
        if max_distance > 0:
            distance = calculate_distance(item_lat, item_lon, lat, lon)
            if distance > max_distance:
                continue
        filtered_data.append(item)
    return jsonify(filtered_data)


if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))
