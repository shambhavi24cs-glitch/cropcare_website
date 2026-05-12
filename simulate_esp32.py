import requests
import time
import random

# Use the local address where app.py is running
BASE_URL = "http://127.0.0.1:5000"

def run_simulation():
    print("--- Virtual ESP32 Simulation Started ---")
    current_soil = 60  # Start with "wet" soil

    while True:
        # 1. Simulate Sensor Readings (Randomized)
        temp = round(random.uniform(25.0, 35.0), 1)
        humidity = round(random.uniform(50.0, 70.0), 1)
        
        # Simulate soil drying over time
        current_soil -= 5 
        if current_soil < 10: current_soil = 80 # Reset if it gets too low

        # 2. Prepare Data (Matching the format in esp32.ino)
        payload = {
            "temp": temp,
            "humidity": humidity,
            "soil": current_soil,
            "device_id": "VIRTUAL-ESP-01"
        }

        try:
            # 3. Post data to the server
            requests.post(f"{BASE_URL}/sensor-data", json=payload)
            print(f"Sent Data -> Temp: {temp}C, Soil: {current_soil}%")

            # 4. Fetch the spray command from the server
            response = requests.get(f"{BASE_URL}/get-command")
            command = response.text
            
            if command == "ON":
                print(">>> STATUS: Sprinkler is ACTIVE (Watering Plants)")
            else:
                print(">>> STATUS: Sprinkler is IDLE")

        except Exception as e:
            print(f"Error connecting to server: {e}")

        # Wait 10 seconds before next update to match dashboard interval
        time.sleep(10)

if __name__ == "__main__":
    run_simulation()