import json
import requests

from flask import Flask, request, jsonify
from flask_sock import Sock

app = Flask(__name__)
sock = Sock(app)

# # Initialize global variables to store coordinates
coordinates = {'x': 300, 'y': 200}  # Default position
x = 0
y = 0

# WebSockets
# @sock.route('/echo')
# def echo(ws):
#     while True:
#         data = ws.receive()
#         ws.send(data)

@sock.route('/')
def echo(ws):
    while True:
        data = ws.receive()
        if data:
            try:
                parsed_data = json.loads(data)
                print("Received data:", parsed_data)
                coordinate = parsed_data.get("coordinate")
                type_value = parsed_data.get("type")

                if coordinate:
                    global x, y
                    x = coordinate.get("x_coordinate")
                    y = coordinate.get("y_coordinate")

                update_data = {
                    'x': x,
                    'y': y
                }

                response = requests.post(
                    'http://127.0.0.1:5000/update_coordinates',
                    json=update_data
                )

                # Check if the request was successful
                if response.status_code == 200:
                    print("INTERNAL MESSAGE: Coordinates updated successfully")
                else:
                    print("INTERNAL MESSAGE: Failed to update coordinates:", response.json())

                response = {
                    "status": "received",
                    "coordinate": coordinate,
                    "type": type_value
                }

                ws.send(json.dumps(response))
            except json.JSONDecodeError:
                print("INTERNAL MESSAGE: some crap got sent")
                ws.send(json.dumps({"error": "Invalid JSON data received"}))

# # Route to update coordinates via POST request
@app.route('/update_coordinates', methods=['POST'])
def update_coordinates():
    global coordinates
    data = request.get_json()
    if 'x' in data and 'y' in data:
        coordinates['x'] = data['x']
        coordinates['y'] = data['y']
        return jsonify({'message': 'Coordinates updated successfully'}), 200
    else:
        return jsonify({'error': 'Invalid coordinates'}), 400

# Route to get the current coordinates via GET request
@app.route('/get_coordinates', methods=['GET'])
def get_coordinates():
    return jsonify(coordinates), 200

if __name__ == '__main__':
    app.run(debug=True)
