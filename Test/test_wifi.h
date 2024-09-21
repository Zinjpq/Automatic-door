#include <WebServer.h>
#include <EEPROM.h>

WebServer server(80);

// Define maximum number of Wi-Fi credentials
const int maxCredentials = 5;

// Structure to hold SSID and password
struct WiFiCredential{
  char ssid[32];
  char password[32];
};

// Save multiple Wi-Fi credentials into EEPROM
void saveWiFiCredentials(WiFiCredential credentials[], int count) {
  EEPROM.begin(512);
  EEPROM.write(0, count); // Save the number of stored credentials at index 0
  
  int address = 1; // Start writing after the count
  for (int i = 0; i < count; i++) {
    for (int j = 0; j < 32; j++) {
      EEPROM.write(address++, credentials[i].ssid[j]);
    }
    for (int j = 0; j < 32; j++) {
      EEPROM.write(address++, credentials[i].password[j]);
    }
  }
  EEPROM.commit();
}

// Load multiple Wi-Fi credentials from EEPROM
int loadWiFiCredentials(WiFiCredential credentials[]) {
  EEPROM.begin(512);
  int count = EEPROM.read(0); // Read the number of stored credentials
  if (count > maxCredentials) count = maxCredentials; // Ensure count doesn't exceed max
  
  int address = 1; // Start reading after the count
  for (int i = 0; i < count; i++) {
    for (int j = 0; j < 32; j++) {
      credentials[i].ssid[j] = EEPROM.read(address++);
    }
    for (int j = 0; j < 32; j++) {
      credentials[i].password[j] = EEPROM.read(address++);
    }
  }
  return count;
}

// Function to handle the root page for Wi-Fi configuration
void handleRoot() {
  String html = "<html><body><h1>Wi-Fi Configuration</h1>";
  html += "<form action='/save' method='POST'>";
  html += "SSID: <input type='text' name='ssid'><br>";
  html += "Password: <input type='text' name='password'><br>";
  html += "<input type='submit' value='Save'>";
  html += "</form></body></html>";

  server.send(200, "text/html", html);
}

// Function to handle saving new Wi-Fi credentials
void handleSave() {
  String ssid = server.arg("ssid");
  String password = server.arg("password");

  // Load existing credentials
  WiFiCredential credentials[maxCredentials];
  int count = loadWiFiCredentials(credentials);

  // Add the new credential (if space allows)
  if (count < maxCredentials) {
    ssid.toCharArray(credentials[count].ssid, 32);
    password.toCharArray(credentials[count].password, 32);
    count++;
    saveWiFiCredentials(credentials, count); // Save updated credentials
    Serial.println("New Wi-Fi Credential Saved!");
  } else {
    Serial.println("No space for additional Wi-Fi credentials!");
  }

  // Notify user and restart
  String message = "<html><body><h1>Wi-Fi Information Saved!</h1><p>ESP32 will now restart.</p></body></html>";
  server.send(200, "text/html", message);

  delay(2000);
  ESP.restart();
}

// Function to display all stored Wi-Fi credentials
void handleViewCredentials() {
  WiFiCredential credentials[maxCredentials];
  int count = loadWiFiCredentials(credentials);

  String html = "<html><body><h1>Stored Wi-Fi Credentials</h1><ul>";
  for (int i = 0; i < count; i++) {
    html += "<li>SSID: " + String(credentials[i].ssid) + "</li>";
  }
  html += "</ul></body></html>";

  server.send(200, "text/html", html);
}

void setup_access_point(){
  WiFi.softAP("ESP32-Access Point", "12345678");
  Serial.println("Access Point mode started");
  Serial.println(WiFi.softAPIP());

  server.on("/", handleRoot); // Homepage
  server.on("/save", HTTP_POST, handleSave); // Save Wi-Fi info
  server.on("/view", handleViewCredentials); // View stored Wi-Fi credentials
  server.begin();
}
