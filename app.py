from flask import Flask, jsonify, request
from datetime import datetime
import pytz
app = Flask(__name__)

API_TOKEN = "supersecrettoken123"

# Sample capital to timezone mapping
capital_timezones = {
    "Washington": "America/New_York",
    "London": "Europe/London",
    "Paris": "Europe/Paris",
    "Tokyo": "Asia/Tokyo",
    "New Delhi": "Asia/Kolkata",
    "Canberra": "Australia/Sydney",
    "Ottawa": "America/Toronto"
}
# Decorator to enforce token check
def token_required(f):
    def decorator(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            if token == API_TOKEN:
                return f(*args, **kwargs)
        return jsonify({"error": "Unauthorized"}), 401
    decorator.__name__ = f.__name__
    return decorator

# Unprotected route
@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({"message": "Hello, world!"})

# Protected route
#@app.route('/api/secure-data', methods=['GET'])
#@token_required
def secure_data():
    return jsonify({"secret": "This is protected info!"})

@app.route('/api/time', methods=['GET'])
@token_required
def get_time():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "Please provide a capital city as a query parameter (e.g., ?city=London)"}), 400

    timezone_name = capital_timezones.get(city)
    if not timezone_name:
        return jsonify({"error": f"City '{city}' not found in database"}), 404

    tz = pytz.timezone(timezone_name)
    local_time = datetime.now(tz)
    utc_offset = local_time.strftime('%z')
    utc_offset_formatted = f"UTC{utc_offset[:3]}:{utc_offset[3:]}"  # Format like UTC+05:30

    return jsonify({
        "city": city,
        "current_time": local_time.strftime('%Y-%m-%d %H:%M:%S'),
        "utc_offset": utc_offset_formatted
    })

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
