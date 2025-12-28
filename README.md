# SamudraManthan - Autonomous Boat Monitoring System

A Flask-based web application for monitoring and controlling ESP32-powered autonomous boats with environmental sensing capabilities.

## 🚢 Features

### Real-time Monitoring
- **Environmental Sensors**: Turbidity, temperature, humidity monitoring
- **Oil Detection**: IR-based oil spill detection with turbidity correlation
- **Waste Detection**: Ultrasonic distance-based waste detection
- **GPS Tracking**: Real-time latitude/longitude positioning
- **Live Dashboard**: Web-based monitoring interface

### Boat Control
- **Dual Mode Operation**: Manual and automatic control modes
- **Thruster Control**: Independent control of two thrusters (-100% to +100%)
- **Failsafe System**: Automatic motor shutdown on communication timeout
- **Mission Planning**: Automated waypoint navigation system

### Communication
- **RESTful API**: HTTP-based communication with ESP32
- **Real-time Updates**: Live sensor data streaming
- **Command Acknowledgment**: Reliable command delivery system
- **Debug Endpoints**: Comprehensive debugging and testing tools

## 🏗️ Project Structure

```
SamudraManthan/
├── app.py                 # Main Flask application
├── templates/
│   ├── index.html         # Boat list dashboard
│   ├── boat.html          # Individual boat control panel
│   └── automated.html     # Mission planning interface
├── .vscode/               # VS Code configuration
└── README.md              # This file
```

## 🔧 Installation

### Prerequisites
- Python 3.7+
- Flask framework
- ESP32 with WiFi capability

### Setup
1. Clone the repository:
```bash
git clone <repository-url>
cd SamudraManthan
```

2. Install dependencies:
```bash
pip install flask
```

3. Run the application:
```bash
python app.py
```

The server will start on `http://0.0.0.0:5000`

## 📡 API Endpoints

### ESP32 Communication

#### POST `/update`
Receive sensor data from ESP32
```json
{
  "boat_id": "boat1",
  "turbidity": 450,
  "ir": "OIL",
  "temperature": 25.5,
  "humidity": 60.2,
  "lat": 12.9716,
  "lon": 77.5946,
  "waste": false,
  "thruster1": 0,
  "thruster2": 0
}
```

#### GET `/command/<boat_id>`
ESP32 fetches motor commands
```json
{
  "thruster1": 50,
  "thruster2": -30,
  "mode": "MANUAL"
}
```

#### POST `/ack`
ESP32 acknowledges command execution
```json
{
  "boat_id": "boat1"
}
```

### Web Interface

#### POST `/motor`
Manual thruster control
```json
{
  "boat": "boat1",
  "motor": "1",
  "value": 75
}
```

#### POST `/mode`
Switch between MANUAL/AUTO modes
```json
{
  "boat": "boat1",
  "mode": "AUTO"
}
```

#### GET `/status/<boat_id>`
Get real-time boat status
```json
{
  "turbidity": 450,
  "temperature": 25.5,
  "oil": true,
  "waste": false,
  "thruster1": 0,
  "thruster2": 0,
  "mode": "MANUAL",
  "online": true,
  "time": "14:30:25"
}
```

### Mission Control

#### POST `/mission/start`
Start automated mission
```json
{
  "base": {"lat": 12.9716, "lon": 77.5946},
  "points": [
    {"lat": 12.9720, "lon": 77.5950},
    {"lat": 12.9725, "lon": 77.5955}
  ]
}
```

#### GET `/mission/status`
Get current mission status

#### POST `/mission/complete`
Mark mission as complete

### Debug Endpoints

#### GET/POST `/test`
Test ESP32 communication

#### GET `/debug/<boat_id>`
Get detailed boat debug information

## ⚙️ Configuration

### Thresholds
```python
TURBIDITY_THRESHOLD = 600    # Oil detection threshold
WASTE_DISTANCE_CM = 200      # Waste detection distance
THRUSTER_TIMEOUT = 5         # Failsafe timeout (seconds)
```

### Detection Logic
- **Oil Detection**: `turbidity < 600 AND ir == "OIL"`
- **Waste Detection**: Distance-based ultrasonic sensing
- **Failsafe**: Motors stop if no ACK received within 5 seconds

## 🌐 Web Interface

### Dashboard Pages
- **`/`** - Main dashboard showing all boats
- **`/boat/<boat_id>`** - Individual boat control panel
- **`/automated`** - Mission planning interface

### Features
- Real-time sensor data display
- Manual thruster control sliders
- Mode switching (Manual/Auto)
- Mission waypoint planning
- Live status indicators

## 🔍 Debugging

### Debug Features
- Comprehensive request logging
- Raw data inspection
- JSON parsing error handling
- Communication timeout monitoring

### Common Issues
1. **400 Error on `/update`**: Check ESP32 JSON format and Content-Type header
2. **Motor Control Not Working**: Verify boat is in MANUAL mode
3. **Failsafe Activation**: Check ESP32 ACK responses and network connectivity

### Debug Commands
```bash
# Test server connectivity
curl http://localhost:5000/test

# Check boat status
curl http://localhost:5000/status/boat1

# Debug boat data
curl http://localhost:5000/debug/boat1
```

## 🤖 ESP32 Integration

### Required Libraries
- WiFi
- HTTPClient
- ArduinoJson
- Sensor libraries (DHT, ultrasonic, etc.)

### Communication Flow
1. ESP32 connects to WiFi
2. Sends sensor data via POST `/update`
3. Fetches commands via GET `/command/<boat_id>`
4. Executes motor commands
5. Sends acknowledgment via POST `/ack`
6. Repeat every loop cycle

### Sample ESP32 Code Structure
```cpp
// Send sensor data
HTTPClient http;
http.begin("http://server:5000/update");
http.addHeader("Content-Type", "application/json");
String payload = "{\"boat_id\":\"boat1\",\"turbidity\":" + String(turbidity) + "}";
http.POST(payload);

// Get commands
http.begin("http://server:5000/command/boat1");
String response = http.getString();
// Parse and execute commands

// Send ACK
http.begin("http://server:5000/ack");
http.POST("{\"boat_id\":\"boat1\"}");
```

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production Deployment
```bash
# Using Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Using Docker
docker build -t samudramanthan .
docker run -p 5000:5000 samudramanthan
```

## 📊 Monitoring

### System Health
- Real-time boat connectivity status
- Sensor data validation
- Communication timeout tracking
- Mission progress monitoring

### Performance Metrics
- Request response times
- Data update frequency
- Failsafe activation count
- Mission completion rates

## 🔒 Security Considerations

- Input validation on all endpoints
- JSON parsing error handling
- Rate limiting (recommended for production)
- HTTPS encryption (recommended for production)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

[Add your license information here]

## 📞 Support

For issues and questions:
- Check the debug endpoints for troubleshooting
- Review the console logs for detailed error information
- Ensure ESP32 and server are on the same network

---

**SamudraManthan** - Autonomous Environmental Monitoring for Marine Conservation
