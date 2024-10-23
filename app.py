# app.py
from flask import Flask, render_template_string
import requests

app = Flask(_name_)

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

@app.route('/')
def home():
    ip_info = get_ip_info()
    if "error" in ip_info:
        return ip_info["error"]
    
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>IP Information</title>
        <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <div class="container mt-5">
            <div class="card">
                <div class="card-body">
                    <h1 class="card-title">IP Information</h1>
                    <ul class="list-group list-group-flush">
                    {% for key, value in ip_info.items() %}
                        <li class="list-group-item"><strong>{{ key }}:</strong> {{ value }}</li>
                    {% endfor %}
                    </ul>
                </div>
            </div>
        </div>
        <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.4/dist/umd/popper.min.js"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    </body>
    </html>
    """
    return render_template_string(html, ip_info=ip_info)

if _name_ == "_main_":
    app.run(debug=True)