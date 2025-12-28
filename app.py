# from flask import Flask, request, render_template, jsonify
# from datetime import datetime

# app = Flask(__name__)

# # =====================================================
# # LIVE DATA STORAGE
# # =====================================================
# boats_data = {}

# # =====================================================
# # THRESHOLDS
# # =====================================================
# TURBIDITY_THRESHOLD = 600
# WASTE_DISTANCE_CM = 25

# # =====================================================
# # RECEIVE DATA FROM ESP32
# # =====================================================
# @app.route('/update', methods=['POST'])
# def update_boat():
#     data = request.json
#     boat_id = data.get("boat_id", "boat1")

#     turbidity   = data.get("turbidity")
#     ir           = data.get("ir")
#     temperature  = data.get("temperature")
#     humidity     = data.get("humidity")
#     lat          = data.get("lat", 0)
#     lon          = data.get("lon", 0)
#     waste        = data.get("waste", False)
#     thruster1    = data.get("thruster1", 0)
#     thruster2    = data.get("thruster2", 0)

#     # ---------- OIL DETECTION ----------
#     oil_detected = (
#         turbidity is not None and
#         turbidity < TURBIDITY_THRESHOLD and
#         ir == "OIL"
#     )

#     # ---------- STORE DATA ----------
#     boats_data[boat_id] = {
#         "turbidity": turbidity,
#         "ir": ir,
#         "temperature": temperature,
#         "humidity": humidity,
#         "lat": lat,
#         "lon": lon,
#         "waste": waste,
#         "oil": oil_detected,
#         "thruster1": thruster1,
#         "thruster2": thruster2,
#         "time": datetime.now().strftime("%H:%M:%S"),
#         "online": True
#     }

#     print(f"[UPDATE] {boat_id} → Data received")
#     return jsonify({"status": "ok"})


# # =====================================================
# # THRUSTER CONTROL FROM WEB
# # =====================================================
# @app.route('/motor', methods=['POST'])
# def motor_control():
#     data = request.json

#     boat_id = data.get("boat", "boat1")
#     motor   = data.get("motor")
#     value   = int(data.get("value", 0))

#     # Initialize boat data if it doesn't exist
#     if boat_id not in boats_data:
#         prev = boats_data.get(boat_id, {})
#         boats_data[boat_id] = {
#             "turbidity": None,
#             "ir": None,
#             "temperature": None,
#             "humidity": None,
#             "lat": 0,
#             "lon": 0,
#             "waste": False,
#             "oil": False,
#             "thruster1": data.get("thruster1", prev.get("thruster1", 0)),
#             "thruster2": data.get("thruster2", prev.get("thruster2", 0)),

#             "time": datetime.now().strftime("%H:%M:%S"),
#             "online": True
#         }

#     # Update thruster values
#     if motor == "1":
#         boats_data[boat_id]["thruster1"] = value
#     elif motor == "2":
#         boats_data[boat_id]["thruster2"] = value

#     # Update timestamp
#     boats_data[boat_id]["time"] = datetime.now().strftime("%H:%M:%S")

#     print(f"[THRUSTER] {boat_id} → M{motor} = {value}% (Updated)")
#     return jsonify({
#         "status": "updated", 
#         "boat_id": boat_id,
#         "motor": motor,
#         "value": value,
#         "thruster1": boats_data[boat_id]["thruster1"],
#         "thruster2": boats_data[boat_id]["thruster2"]
#     })


# # =====================================================
# # ESP32 FETCHES COMMAND
# # =====================================================
# @app.route('/command/<boat_id>')
# def get_command(boat_id):
#     boat = boats_data.get(boat_id, {})
#     command_data = {
#         "thruster1": boat.get("thruster1", 0),
#         "thruster2": boat.get("thruster2", 0)
#     }
#     print(f"[COMMAND] ESP32 {boat_id} fetching → T1:{command_data['thruster1']}% T2:{command_data['thruster2']}%")
#     return jsonify(command_data)


# # =====================================================
# # DEBUG ENDPOINT - Check all boat data
# # =====================================================
# @app.route('/debug/<boat_id>')
# def debug_boat(boat_id):
#     boat = boats_data.get(boat_id, {})
#     return jsonify({
#         "boat_id": boat_id,
#         "exists": boat_id in boats_data,
#         "data": boat,
#         "all_boats": list(boats_data.keys())
#     })


# # =====================================================
# # DASHBOARD ROUTES
# # =====================================================
# @app.route('/')
# def boats_list():
#     return render_template("index.html", boats=boats_data)


# @app.route('/boat/<boat_id>')
# def boat_dashboard(boat_id):
#     boat = boats_data.get(boat_id, {
#         "turbidity": "---",
#         "ir": "---",
#         "temperature": "---",
#         "humidity": "---",
#         "lat": 0,
#         "lon": 0,
#         "oil": False,
#         "waste": False,
#         "thruster1": 0,
#         "thruster2": 0,
#         "time": "---",
#         "online": False
#     })
#     return render_template("boat.html", boat=boat, bid=boat_id)


# # =====================================================
# # LIVE STATUS API (FIXED)
# # =====================================================
# @app.route('/status/<boat_id>')
# def boat_status(boat_id):
#     boat = boats_data.get(boat_id)
#     return jsonify(boat if boat else {})


# # =====================================================
# # SERVER RUN
# # =====================================================
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)


# from flask import Flask, request, render_template, jsonify
# from datetime import datetime

# app = Flask(__name__)

# # =====================================================
# # LIVE DATA STORAGE
# # =====================================================
# boats_data = {}

# # =====================================================
# # THRESHOLDS
# # =====================================================
# TURBIDITY_THRESHOLD = 600
# WASTE_DISTANCE_CM = 25


# # =====================================================
# # RECEIVE DATA FROM ESP32
# # =====================================================
# @app.route('/update', methods=['POST'])
# def update_boat():
#     data = request.json
#     boat_id = data.get("boat_id", "boat1")

#     prev = boats_data.get(boat_id, {})

#     turbidity   = data.get("turbidity")
#     ir           = data.get("ir")
#     temperature  = data.get("temperature")
#     humidity     = data.get("humidity")
#     lat          = data.get("lat", 0)
#     lon          = data.get("lon", 0)
#     waste        = data.get("waste", False)

#     # ---------- OIL DETECTION ----------
#     oil_detected = (
#         turbidity is not None and
#         turbidity < TURBIDITY_THRESHOLD and
#         ir == "OIL"
#     )

#     # ---------- STORE DATA (CRITICAL FIX HERE) ----------
#     boats_data[boat_id] = {
#         "turbidity": turbidity,
#         "ir": ir,
#         "temperature": temperature,
#         "humidity": humidity,
#         "lat": lat,
#         "lon": lon,
#         "waste": waste,
#         "oil": oil_detected,

#         # 🔥 KEEP LAST WEB-COMMAND VALUES
#         "thruster1": data.get("thruster1", prev.get("thruster1", 0)),
#         "thruster2": data.get("thruster2", prev.get("thruster2", 0)),

#         "time": datetime.now().strftime("%H:%M:%S"),
#         "online": True
#     }

#     print(f"[UPDATE] {boat_id} → ESP32 data received")
#     return jsonify({"status": "ok"})


# # =====================================================
# # THRUSTER CONTROL FROM WEB
# # =====================================================
# @app.route('/motor', methods=['POST'])
# def motor_control():
#     data = request.json

#     boat_id = data.get("boat", "boat1")
#     motor   = data.get("motor")
#     value   = int(data.get("value", 0))

#     # ---------- INIT BOAT IF NOT EXISTS ----------
#     if boat_id not in boats_data:
#         boats_data[boat_id] = {
#             "turbidity": None,
#             "ir": None,
#             "temperature": None,
#             "humidity": None,
#             "lat": 0,
#             "lon": 0,
#             "waste": False,
#             "oil": False,
#             "thruster1": 0,
#             "thruster2": 0,
#             "time": datetime.now().strftime("%H:%M:%S"),
#             "online": True
#         }

#     # ---------- UPDATE THRUSTER ----------
#     if motor == "1":
#         boats_data[boat_id]["thruster1"] = value
#     elif motor == "2":
#         boats_data[boat_id]["thruster2"] = value

#     boats_data[boat_id]["time"] = datetime.now().strftime("%H:%M:%S")

#     print(f"[THRUSTER] {boat_id} → M{motor} = {value}%")

#     return jsonify({
#         "status": "updated",
#         "boat_id": boat_id,
#         "motor": motor,
#         "value": value,
#         "thruster1": boats_data[boat_id]["thruster1"],
#         "thruster2": boats_data[boat_id]["thruster2"]
#     })


# # =====================================================
# # ESP32 FETCHES COMMAND
# # =====================================================
# @app.route('/command/<boat_id>')
# def get_command(boat_id):
#     boat = boats_data.get(boat_id, {})

#     command_data = {
#         "thruster1": boat.get("thruster1", 0),
#         "thruster2": boat.get("thruster2", 0)
#     }

#     print(
#         f"[COMMAND] ESP32 {boat_id} → "
#         f"T1:{command_data['thruster1']}% "
#         f"T2:{command_data['thruster2']}%"
#     )

#     return jsonify(command_data)


# # =====================================================
# # DEBUG ENDPOINT
# # =====================================================
# @app.route('/debug/<boat_id>')
# def debug_boat(boat_id):
#     return jsonify({
#         "boat_id": boat_id,
#         "exists": boat_id in boats_data,
#         "data": boats_data.get(boat_id, {}),
#         "all_boats": list(boats_data.keys())
#     })


# # =====================================================
# # DASHBOARD ROUTES
# # =====================================================
# @app.route('/')
# def boats_list():
#     return render_template("index.html", boats=boats_data)


# @app.route('/boat/<boat_id>')
# def boat_dashboard(boat_id):
#     boat = boats_data.get(boat_id, {
#         "turbidity": "---",
#         "ir": "---",
#         "temperature": "---",
#         "humidity": "---",
#         "lat": 0,
#         "lon": 0,
#         "oil": False,
#         "waste": False,
#         "thruster1": 0,
#         "thruster2": 0,
#         "time": "---",
#         "online": False
#     })
#     return render_template("boat.html", boat=boat, bid=boat_id)


# # =====================================================
# # LIVE STATUS API
# # =====================================================
# @app.route('/status/<boat_id>')
# def boat_status(boat_id):
#     return jsonify(boats_data.get(boat_id, {}))


# # =====================================================
# # SERVER RUN
# # =====================================================
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)


# from flask import Flask, request, render_template, jsonify
# from datetime import datetime
# import time

# app = Flask(__name__)

# # =====================================================
# # CONFIG
# # =====================================================
# THRUSTER_TIMEOUT = 5  # seconds

# # =====================================================
# # LIVE DATA STORAGE
# # =====================================================
# boats_data = {}

# # =====================================================
# # HELPER: INIT BOAT
# # =====================================================
# def init_boat(boat_id):
#     if boat_id not in boats_data:
#         boats_data[boat_id] = {
#             "thruster1": 0,
#             "thruster2": 0,
#             "mode": "MANUAL",        # MANUAL / AUTO
#             "last_ack": 0,
#             "online": True,
#             "time": datetime.now().strftime("%H:%M:%S")
#         }

# # =====================================================
# # RECEIVE SENSOR DATA FROM ESP32
# # (AUTO MODE ONLY)
# # =====================================================
# @app.route('/update', methods=['POST'])
# def update_boat():
#     data = request.json
#     boat_id = data.get("boat_id", "boat1")
#     init_boat(boat_id)

#     # 🚫 BLOCK ESP32 MOTOR UPDATE IN MANUAL MODE
#     if boats_data[boat_id]["mode"] == "AUTO":
#         boats_data[boat_id]["thruster1"] = data.get(
#             "thruster1", boats_data[boat_id]["thruster1"]
#         )
#         boats_data[boat_id]["thruster2"] = data.get(
#             "thruster2", boats_data[boat_id]["thruster2"]
#         )

#     boats_data[boat_id]["time"] = datetime.now().strftime("%H:%M:%S")
#     boats_data[boat_id]["online"] = True

#     return jsonify({"status": "ok"})


# # =====================================================
# # MANUAL MOTOR CONTROL (WEB)
# # =====================================================
# @app.route('/motor', methods=['POST'])
# def motor_control():
#     data = request.json
#     boat_id = data.get("boat", "boat1")
#     motor = data.get("motor")
#     value = int(data.get("value", 0))

#     init_boat(boat_id)

#     # 🔒 ONLY ALLOWED IN MANUAL MODE
#     if boats_data[boat_id]["mode"] != "MANUAL":
#         return jsonify({"error": "Boat in AUTO mode"}), 403

#     if motor == "1":
#         boats_data[boat_id]["thruster1"] = value
#     elif motor == "2":
#         boats_data[boat_id]["thruster2"] = value

#     boats_data[boat_id]["time"] = datetime.now().strftime("%H:%M:%S")

#     print(f"[MANUAL] {boat_id} → T1:{boats_data[boat_id]['thruster1']} T2:{boats_data[boat_id]['thruster2']}")

#     return jsonify({"status": "updated"})


# # =====================================================
# # MODE SWITCH (MANUAL / AUTO)
# # =====================================================
# @app.route('/mode', methods=['POST'])
# def set_mode():
#     data = request.json
#     boat_id = data.get("boat", "boat1")
#     mode = data.get("mode", "MANUAL")

#     init_boat(boat_id)

#     boats_data[boat_id]["mode"] = mode
#     print(f"[MODE] {boat_id} → {mode}")

#     return jsonify({"status": "ok", "mode": mode})


# # =====================================================
# # ESP32 FETCHES COMMAND
# # =====================================================
# @app.route('/command/<boat_id>')
# def get_command(boat_id):
#     init_boat(boat_id)

#     # ⏱ FAILSAFE CHECK
#     now = time.time()
#     if now - boats_data[boat_id]["last_ack"] > THRUSTER_TIMEOUT:
#         boats_data[boat_id]["thruster1"] = 0
#         boats_data[boat_id]["thruster2"] = 0
#         print(f"[FAILSAFE] {boat_id} motors stopped!")

#     return jsonify({
#         "thruster1": boats_data[boat_id]["thruster1"],
#         "thruster2": boats_data[boat_id]["thruster2"],
#         "mode": boats_data[boat_id]["mode"]
#     })


# # =====================================================
# # ESP32 ACK CONFIRMATION
# # =====================================================
# @app.route('/ack', methods=['POST'])
# def ack():
#     data = request.json
#     boat_id = data.get("boat_id", "boat1")

#     init_boat(boat_id)

#     boats_data[boat_id]["last_ack"] = time.time()
#     print(f"[ACK] {boat_id} motors applied")

#     return jsonify({"status": "ack_received"})


# # =====================================================
# # DEBUG
# # =====================================================
# @app.route('/debug/<boat_id>')
# def debug(boat_id):
#     return jsonify(boats_data.get(boat_id, {}))


# # =====================================================
# # RUN SERVER
# # =====================================================
# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, debug=True)



from flask import Flask, request, render_template, jsonify
from datetime import datetime
import time

app = Flask(__name__)

# =====================================================
# CONFIG
# =====================================================
THRUSTER_TIMEOUT = 5        # seconds (failsafe)
TURBIDITY_THRESHOLD = 600
WASTE_DISTANCE_CM = 200

# =====================================================
# LIVE DATA STORAGE
# =====================================================
boats_data = {}

# =====================================================
# HELPER: INIT BOAT
# =====================================================
def init_boat(boat_id):
    if boat_id not in boats_data:
        boats_data[boat_id] = {
            # ---- Sensors ----
            "turbidity": None,
            "ir": None,
            "temperature": None,
            "humidity": None,
            "lat": 0,
            "lon": 0,
            "waste": False,
            "oil": False,

            # ---- Motors ----
            "thruster1": 0,
            "thruster2": 0,

            # ---- Control ----
            "mode": "MANUAL",     # MANUAL / AUTO
            "last_ack": 0,

            # ---- Status ----
            "online": True,
            "time": datetime.now().strftime("%H:%M:%S")
        }

# =====================================================
# RECEIVE SENSOR DATA FROM ESP32
# (ESP32 NEVER OVERWRITES THRUSTERS IN MANUAL MODE)
# =====================================================
@app.route('/update', methods=['POST'])
def update_boat():
    data = request.json
    boat_id = data.get("boat_id", "boat1")
    init_boat(boat_id)

    turbidity = data.get("turbidity")
    ir = data.get("ir")
    temperature = data.get("temperature")
    humidity = data.get("humidity")
    lat = data.get("lat", 0)
    lon = data.get("lon", 0)
    waste = data.get("waste", False)

    # ---- Oil detection ----
    oil_detected = (
        turbidity is not None and
        turbidity < TURBIDITY_THRESHOLD and
        ir == "OIL"
    )

    boat = boats_data[boat_id]

    # ---- Store sensor data ----
    boat["turbidity"] = turbidity
    boat["ir"] = ir
    boat["temperature"] = temperature
    boat["humidity"] = humidity
    boat["lat"] = lat
    boat["lon"] = lon
    boat["waste"] = waste
    boat["oil"] = oil_detected

    # ---- AUTO MODE: allow ESP32 thruster update ----
    if boat["mode"] == "AUTO":
        boat["thruster1"] = data.get("thruster1", boat["thruster1"])
        boat["thruster2"] = data.get("thruster2", boat["thruster2"])

    boat["online"] = True
    boat["time"] = datetime.now().strftime("%H:%M:%S")

    print(f"[UPDATE] {boat_id} sensor data received")
    return jsonify({"status": "ok"})

# =====================================================
# MANUAL MOTOR CONTROL (WEB)
# =====================================================
@app.route('/motor', methods=['POST'])
def motor_control():
    data = request.json
    boat_id = data.get("boat", "boat1")
    motor = data.get("motor")
    value = int(data.get("value", 0))

    init_boat(boat_id)
    boat = boats_data[boat_id]

    # ---- Lock in AUTO mode ----
    if boat["mode"] != "MANUAL":
        return jsonify({"error": "Boat in AUTO mode"}), 403

    if motor == "1":
        boat["thruster1"] = value
    elif motor == "2":
        boat["thruster2"] = value

    boat["time"] = datetime.now().strftime("%H:%M:%S")

    print(f"[MANUAL] {boat_id} → T1:{boat['thruster1']}% T2:{boat['thruster2']}%")
    return jsonify({
        "status": "updated",
        "thruster1": boat["thruster1"],
        "thruster2": boat["thruster2"]
    })

# =====================================================
# MODE SWITCH (MANUAL / AUTO)
# =====================================================
@app.route('/mode', methods=['POST'])
def set_mode():
    data = request.json
    boat_id = data.get("boat", "boat1")
    mode = data.get("mode", "MANUAL")

    if mode not in ["MANUAL", "AUTO"]:
        return jsonify({"error": "Invalid mode"}), 400

    init_boat(boat_id)
    boats_data[boat_id]["mode"] = mode

    print(f"[MODE] {boat_id} → {mode}")
    return jsonify({"status": "ok", "mode": mode})

# =====================================================
# ESP32 FETCHES COMMAND
# =====================================================
@app.route('/command/<boat_id>')
def get_command(boat_id):
    init_boat(boat_id)
    boat = boats_data[boat_id]

    # ---- FAILSAFE ----
    now = time.time()
    if now - boat["last_ack"] > THRUSTER_TIMEOUT:
        boat["thruster1"] = 0
        boat["thruster2"] = 0
        print(f"[FAILSAFE] {boat_id} motors STOPPED")

    return jsonify({
        "thruster1": boat["thruster1"],
        "thruster2": boat["thruster2"],
        "mode": boat["mode"]
    })

# =====================================================
# ESP32 ACK CONFIRMATION
# =====================================================
@app.route('/ack', methods=['POST'])
def ack():
    data = request.json
    boat_id = data.get("boat_id", "boat1")

    init_boat(boat_id)
    boats_data[boat_id]["last_ack"] = time.time()

    print(f"[ACK] {boat_id} thrusters applied")
    return jsonify({"status": "ack_received"})

# =====================================================
# STATUS API (FOR LIVE DASHBOARD)
# =====================================================
@app.route('/status/<boat_id>')
def status(boat_id):
    init_boat(boat_id)
    return jsonify(boats_data[boat_id])

# =====================================================
# DEBUG API
# =====================================================
@app.route('/debug/<boat_id>')
def debug(boat_id):
    return jsonify({
        "boat_id": boat_id,
        "exists": boat_id in boats_data,
        "data": boats_data.get(boat_id, {}),
        "all_boats": list(boats_data.keys())
    })

# =====================================================
# BASIC DASHBOARD ROUTES (OPTIONAL)
# =====================================================
@app.route('/')
def index():
    return render_template("index.html", boats=boats_data)

@app.route('/boat/<boat_id>')
def boat_dashboard(boat_id):
    init_boat(boat_id)
    return render_template("boat.html", boat=boats_data[boat_id], bid=boat_id)

mission_data = {
    "base": None,
    "points": [],
    "status": "IDLE"
}

# =====================================================
# ROUTES
# =====================================================
@app.route('/automated')
def automated():
    return render_template("automated.html")  # Your HTML file above should be saved as templates/index.html

# ================= START MISSION =================
@app.route('/mission/start', methods=['POST'])
def start_mission():
    global mission_data
    data = request.json
    mission_data["base"] = data.get("base")
    mission_data["points"] = data.get("points", [])
    mission_data["status"] = "RUNNING"
    print(f"[MISSION START] Base: {mission_data['base']}, Points: {mission_data['points']}")
    return jsonify({"status": "mission started", "points": mission_data["points"]})

# ================= COMPLETE MISSION =================
@app.route('/mission/complete', methods=['POST'])
def complete_mission():
    global mission_data
    mission_data["status"] = "COMPLETE"
    print("[MISSION COMPLETE]")
    return jsonify({"status": "mission complete"})

# ================= GET MISSION STATUS =================
@app.route('/mission/status')
def mission_status():
    return jsonify(mission_data)

# =====================================================
# RUN SERVER
# =====================================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
