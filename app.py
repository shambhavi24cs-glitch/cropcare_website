from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3, datetime

def init_db():
    conn = sqlite3.connect('cropcare.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS sensor_logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        device_id TEXT,
                        temp REAL,
                        humidity REAL,
                        soil REAL,
                        timestamp DATETIME
                    )''')
    conn.commit()
    conn.close()

init_db()

app = Flask(__name__)
CORS(app)  # allows your website to call the API

spray_command = "OFF"  # global state — set by dashboard

# ESP32 sends sensor data here
@app.route('/sensor-data', methods=['POST'])
def receive_sensor_data():
    data = request.json
    conn = sqlite3.connect('cropcare.db')
    conn.execute('''INSERT INTO sensor_logs 
                    (device_id, temp, humidity, soil, timestamp)
                    VALUES (?,?,?,?,?)''',
                 (data['device_id'], data['temp'],
                  data['humidity'], data['soil'],
                  datetime.datetime.now()))
    conn.commit()

    # Auto-spray logic: if soil < 40%, command ON
    global spray_command
    if data['soil'] < 40:
        spray_command = "ON"
    else:
        spray_command = "OFF"

    return jsonify({"status": "ok"})

# ESP32 polls this to know whether to spray
@app.route('/get-command', methods=['GET'])
def get_command():
    return spray_command  # returns plain "ON" or "OFF"

# Dashboard reads latest sensor values
@app.route('/latest', methods=['GET'])
def get_latest():
    conn = sqlite3.connect('cropcare.db')
    row = conn.execute('''SELECT * FROM sensor_logs 
                          ORDER BY timestamp DESC LIMIT 1''').fetchone()
    if row:
        return jsonify({"temp": row[2], "humidity": row[3], "soil": row[4]})
    else:
        return jsonify({"temp": "--", "humidity": "--", "soil": "--"})

# Dashboard manually overrides spray
@app.route('/spray-on', methods=['POST'])
def spray_on():
    global spray_command
    spray_command = "ON"
    return jsonify({"status": "spray activated"})

@app.route('/spray-off', methods=['POST'])
def spray_off():
    global spray_command
    spray_command = "OFF"
    return jsonify({"status": "spray stopped"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # 0.0.0.0 = accessible on local network