from pymodbus.client.sync import ModbusTcpClient

def start_device(device_id, device_config):
    modbus_client = ModbusTcpClient(device_config["ip_address"], device_config["port"])
    
    while True:
        # Get data from device using Modbus TCP protocol
        power_setting_percent = modbus_client.read_input_registers(0, 1).registers[0]
        power_setting_watts = modbus_client.read_input_registers(1, 1).registers[0]
        sensor_data_watts = modbus_client.read_input_registers(2, 1).registers[0]
        sensor_data_volts = modbus_client.read_input_registers(3, 1).registers[0]
        sensor_data_amps = modbus_client.read_input_registers(4, 1).registers[0]
        electric_phase = "L1"

        # Update device data
        data = {
            "power_setting_percent": power_setting_percent,
            "power_setting_watts": power_setting_watts,
            "sensor_data_watts": sensor_data_watts,
            "sensor_data_volts": sensor_data_volts,
            "sensor_data_amps": sensor_data_amps,
            "electric_phase": electric_phase
        }
        socketio.emit('device_data_update', {'device_id': device_id, 'data': data})
        time.sleep(1)
