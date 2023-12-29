from flask import Flask, jsonify, request
import psutil
import requests

app = Flask(__name__)

# Bearer token for authorization
EXPECTED_TOKEN = 'VN6725573818142048'

@app.before_request
def check_auth():
    # Check for Bearer token in Authorization header
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Unauthorized'}), 401

    token = auth_header.split(' ')[1]
    if token != EXPECTED_TOKEN:
        return jsonify({'error': 'Unauthorized'}), 401

@app.route('/status', methods=['GET'])
def get_server_status():
    # Get CPU usage
    cpu_usage = psutil.cpu_percent()

    # Get RAM usage
    ram_info = psutil.virtual_memory()
    ram_used = bytes2human(ram_info.used)
    ram_total = bytes2human(ram_info.total)

    # Get storage usage
    storage_info = psutil.disk_usage('/')
    storage_used = bytes2human(storage_info.used)
    storage_total = bytes2human(storage_info.total)

    # Get public IP address
    public_ip = get_public_ip()

    # Prepare the response
    response = {
        'cpu_usage': cpu_usage,
        'ram_usage': f"{ram_used}/{ram_total}",
        'storage_usage': f"{storage_used}/{storage_total}",
        'public_ip': public_ip
    }

    return jsonify(response)

def get_public_ip():
    try:
        # Get public IP address by making a request to an external API
        response = requests.get('https://api64.ipify.org?format=json')
        if response.status_code == 200:
            public_ip = response.json()['ip']
            return public_ip
        else:
            return "Unable to retrieve public IP"
    except Exception as e:
        return str(e)

def bytes2human(n):
    # Convert bytes to human-readable format
    symbols = ('B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB')
    prefix = {}
    for i, s in enumerate(symbols[1:]):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols[1:]):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return f"{value:.2f} {s}"
    return f"{n} B"

if __name__ == '__main__':
    app.run(debug=False, host= '172.31.4.111', port= 2910)
