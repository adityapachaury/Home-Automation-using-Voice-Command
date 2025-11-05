#include <ESP8266WiFi.h>

#define RELAY_PIN D1  // Relay input pin

const char* ssid = "Airtel_mohi_1015";
const char* password = "Air@29485";
// const char* ssid = "NHR";
// const char* password = "11111111";
// const char* ssid = "Moto 60";
// const char* password = "aditya012012";

WiFiServer server(80);

void setup() {
  Serial.begin(115200);
  pinMode(RELAY_PIN, OUTPUT);

  // Relay OFF initially (Active LOW)
  digitalWrite(RELAY_PIN, HIGH);

  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\n WiFi Connected!");
  Serial.print(" IP Address: ");
  Serial.println(WiFi.localIP());

  server.begin();
}

void loop() {
  WiFiClient client = server.available();
  if (!client) return;

  String request = client.readStringUntil('\r');
  Serial.println(request);
  client.flush();

  if (request.indexOf("/ON") != -1) {
    digitalWrite(RELAY_PIN, LOW);  // Active LOW → ON
    Serial.println("💡 Relay ON");
  }
  else if (request.indexOf("/OFF") != -1) {
    digitalWrite(RELAY_PIN, HIGH); // Active LOW → OFF
    Serial.println("💡 Relay OFF");
  }

  // // Send HTTP response properly
  // client.println("HTTP/1.1 200 OK");
  // client.println("Content-Type: text/html");
  // client.println("Connection: close");  //  add this line to fix 10054 error
  // client.println("");
  // client.println("<h1>Relay Command Executed</h1>");
  // delay(1);  // short delay to allow client to receive data
  client.stop();
}
