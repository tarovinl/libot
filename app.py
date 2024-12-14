# app.py
from venv import logger
from flask import Flask, jsonify, render_template_string, request
import geopy.distance
import requests
import logging
from flask import render_template
import math

app = Flask(__name__)



def get_ip_info():
    try:
        response = requests.get('https://ipinfo.io/json')
        response.raise_for_status()
        data = response.json()
        
        ip_info = {
            "Where you are": data.get("city") + ', ' + data.get("region") + ', ' + data.get("country") ,
            "Check your coordinates": data.get("loc"),
            "Check your IP": data.get("ip"),
            "What did you use?": data.get("org"),
            "Postal Code": data.get("postal"),
            "Timezone": data.get("timezone"),
        }
        
        return ip_info

          
        if not ip_info["Location"]:
            ip_info["Location"] = "0,0"  

        return ip_info

    except requests.RequestException as e:
        return {"error": f"Error fetching IP information: {e}"}

    
@app.route('/calculate_distance', methods=['POST'])
def calculate_distance():
    data = request.get_json()  # Get JSON data from request
    points = data['points']  # Expecting points to be a list of lat/lng tuples
    total_distance = 0.0

    for i in range(1, len(points)):
        total_distance += geopy.distance.distance(points[i-1], points[i]).meters

    return jsonify({'total_distance': total_distance})

@app.route('/homepage')
def homepage():
    return render_template('homepage.html', title='Home - LIBOT')

@app.errorhandler(Exception)
def handle_exception(e):
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.exception(f"An error occurred: {str(e)}")
    return render_template_string('error.html', error_message=str(e)), 500

@app.route('/')
def index():
    ip_info = get_ip_info()
    if "error" in ip_info:
        return ip_info["error"]
    
    return render_template('index.html', ip_info=ip_info)
if __name__ == "__main__":
    app.run(debug=True)
