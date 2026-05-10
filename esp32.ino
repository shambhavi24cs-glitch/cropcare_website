#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>

// --- Config ---
const char* ssid     = "YOUR_WIFI_NAME";
const char* password = "YOUR_WIFI_PASSWORD";
const char* serverURL = "http://172.16.29.107:5000/sensor-data";
const char* commandURL = "http://172.16.29.107:5000/get-command";

#define DHT_PIN 4
#define SOIL_PIN 34       // Analog pin
#define SERVO_PIN 18

DHT dht(DHT_PIN, DHT22);

void setup() {
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) delay(500);
  dht.begin();
  // servo setup...
}

void loop() {
  float temp     = dht.readTemperature();
  float humidity = dht.readHumidity();
  int   soilRaw  = analogRead(SOIL_PIN);
  int   soilPct  = map(soilRaw, 4095, 0, 0, 100); // calibrate these values

  // --- SEND sensor data to server ---
  HTTPClient http;
  http.begin(serverURL);
  http.addHeader("Content-Type", "application/json");
  String body = "{\"temp\":" + String(temp) +
                ",\"humidity\":" + String(humidity) +
                ",\"soil\":" + String(soilPct) +
                ",\"device_id\":\"ESP32-001\"}";
  http.POST(body);
  http.end();

  // --- CHECK if server wants spray ON or OFF ---
  http.begin(commandURL);
  int httpCode = http.GET();
  String response = "";
  if (httpCode > 0) {
    response = http.getString(); // returns "ON" or "OFF"
  }
  http.end();

  if (response == "ON") activateServo();
  else                  deactivateServo();

  delay(30000); // repeat every 30 seconds
}

void activateServo() {
  // Add your servo activation code here
}

void deactivateServo() {
  // Add your servo deactivation code here
}