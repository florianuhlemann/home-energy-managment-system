import time
import threading
import json
import importlib
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Device configurations
device_configs = {
    "adjustable_heater": {
        "module": "adjustable_heater_module",
        "ip_address": "192.168.1.10",
        "port": 502,
        "protocol": "modbus_tcp"
    },
    "electric_charging_station": {
        "module": "electric_charging_station_module",
        "ip_address": "192.168.1.20",
        "port": 8080,
        "protocol": "http_rest"
    },
    "home_battery_system": {
        "module": "home_battery_system_module",
        "ip_address": "192.168.1.30",
        "port": 3671,
        "protocol": "knx"
    }
}

# Device data
device_data = {
    "adjustable_heater": {
        "power_setting_percent": 0,
        "power_setting_watts": 0,
        "sensor_data_watts": 0,
        "sensor_data_volts": 0,
        "sensor_data_amps": 0,
        "electric_phase": "L1"
    },
    "electric_charging_station": {
        "charge_current_amps": 0,
        "power_setting_watts": 0,
        "sensor_data_watts": 0,
        "sensor_data_volts": 0,
        "sensor_data_amps": 0,
        "electric_phase": "L2"
    },
    "home_battery_system": {
        "power_setting_watts": 0,
        "sensor_data_watts": 0,
        "sensor_data_volts": 0,
        "sensor_data_amps": 0,
        "electric_phase": "L3"
    }
}

# Device data locks
device_data_locks = {
    "adjustable_heater": threading.Lock(),
    "electric_charging_station": threading.Lock(),
    "home_battery_system": threading.Lock()
}

# Function to update device data
def update_device_data(device_id, data):
    with device_data_locks[device_id]:
        device_data[device_id].update(data)

# Function to get device data
def get_device_data(device_id):
    with device_data_locks[device_id]:
        return device_data[device_id]

# Function to load device module
def load_device_module(module_name):
    module_path = f"modules.{module_name}"
    module = importlib.import_module(module_path)
    return module

# Function to start device threads
def start_device_threads():
    for device_id, device_config in device_configs.items():
        module_name = device_config["module"]
        module = load_device_module(module_name)
        device_thread = threading.Thread(target=module.start_device, args=(device_id, device_config))
        device_thread.start()

# Function to start calculation thread
def start_calculation_thread():
    calculation_thread = threading.Thread(target=calculate_energy_allocations)
    calculation_thread.start()

# API route to get all device data
@app.route('/api/devices', methods=['GET'])
def get_devices():
    return jsonify(device_data)

# SocketIO event handler for device data update
@socketio.on('device_data_update')
def handle_device_data_update(data):
    device_id = data["device_id"]
    device_data = data["data"]
    update_device_data(device_id, device_data)
    emit('device_data', {'device_id': device_id, 'data': device_data}, broadcast=True)

# Socket Function to start the Flask-SocketIO server
def start_server():
    socketio.run(app, host='0.0.0.0', port=5000)

def calculate_energy_allocations():
    while True:
        # Perform energy allocation calculations
        # ...

        # Update device data
        # ...

        # Emit updated data to clients
        socketio.emit('device_data_update', {'device_id': device_id, 'data': data})

        # Sleep for fixed frequency
        time.sleep(1/frequency)

if __name__ == 'main':
    start_calculation_thread()
    start_device_threads()
    start_server()

start_calculation_thread()
start_device_threads()
start_server()