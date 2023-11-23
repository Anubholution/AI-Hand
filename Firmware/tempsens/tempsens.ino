//https://script.google.com/macros/s/AKfycbwQcwDO_jWiWSTPls1oJxEYuw2tIDWF5ekuGDpD24xpP4cBtYPAs1ywTB_cRc-OIqxxaw/exec
#include <Wire.h>
#include <Adafruit_MLX90614.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <WiFiClientSecure.h>
// Replace with your network details
const char* ssid = "Techolution";
const char* password = "wearethebest";
const char* serverUrl = "https://script.google.com/macros/s/AKfycbwQcwDO_jWiWSTPls1oJxEYuw2tIDWF5ekuGDpD24xpP4cBtYPAs1ywTB_cRc-OIqxxaw/exec";
Adafruit_MLX90614 mlx = Adafruit_MLX90614();
WiFiClientSecure client; // Use WiFiClientSecure for HTTPS
void setup()
{
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
  mlx.begin();
}
double readTemperature()
{
  double temperature = mlx.readObjectTempC();
  Serial.print("Temperature: ");
  Serial.println(temperature);
  return temperature;
}
void sendDataToSheet(double temperature)
{
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    client.setTimeout(10000); // Optional: Increase timeout
    String url = serverUrl + String("?temperature=") + String(temperature);
    Serial.print("Connecting to: ");
    Serial.println(url);
    if (http.begin(client, url)) { // Use WiFiClientSecure here
      int httpCode = http.GET();
      Serial.print("HTTP Response Code: ");
      Serial.println(httpCode);
      if (httpCode > 0) {
        String payload = http.getString();
        Serial.print("Response: ");
        Serial.println(payload);
      } else {
        Serial.print("GET request failed. Error: ");
        Serial.println(http.errorToString(httpCode));
      }
      http.end();
    } else {
      Serial.println("Unable to begin HTTP");
    }
  } else {
    Serial.println("Not connected to WiFi");
  }
}
void loop()
{
  double temperature = readTemperature();
  sendDataToSheet(temperature);
  delay(60000/2);
}
