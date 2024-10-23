# app.py
from venv import logger
from flask import Flask, render_template_string
import requests
import logging
from flask import render_template

app = Flask(__name__)

def get_ip_info():
    try:
        response = requests.get('https://ipinfo.io/json')
        response.raise_for_status()
        data = response.json()
        
        ip_info = {
            "IP Address": data.get("ip"),
            "Hostname": data.get("hostname"),
            "City": data.get("city"),
            "Region": data.get("region"),
            "Country": data.get("country"),
            "Location": data.get("loc"),
            "Organization": data.get("org"),
            "Postal": data.get("postal"),
            "Timezone": data.get("timezone"),
            "ASN": data.get("asn", {}).get("asn"),
            "ISP": data.get("asn", {}).get("name")
        }
        
        return ip_info
    
    except requests.RequestException as e:
        return {"error": f"Error fetching IP information: {e}"}

@app.route('/homepage')
def homepage():
    return render_template('homepage.html', title='Home - LIBOT')

@app.errorhandler(Exception)
def handle_exception(e):
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.exception(f"An error occurred: {str(e)}")
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Error</title>
    </head>
    <body>
        <h1>An error occurred</h1>
        <p>{error_message}</p>
    </body>
    </html>
    """, error_message=str(e)), 500

@app.route('/')
def index():
    ip_info = get_ip_info()
    if "error" in ip_info:
        return ip_info["error"]
    
    return render_template('index.html', ip_info=ip_info)
if __name__ == "__main__":
    app.run(debug=True)