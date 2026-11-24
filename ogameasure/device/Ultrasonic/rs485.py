from pymodbus.client import ModbusTcpClient

class rs485(object):
    def __init__(self, ip_address, port):
        self.client = ModbusTcpClient(ip_address, port=port)

        if not self.client.connect():
            print("Connection failed")
            exit(1)
        else:
            print("Connected!")

    def get_temp(self):
        temp = self.client.read_holding_registers(address=0x01f9, count=1)
        temp_value = temp.registers[0]/10

        return temp_value

    def get_humid(self):
        humid = self.client.read_holding_registers(address=0x01f8, count=1)
        humid_value = humid.registers[0]/10

        return humid_value

    def get_wind_speed(self):
        wind_speed = self.client.read_holding_registers(address=0x01f4, count=1)
        wind_speed_value = wind_speed.registers[0]/10

        return wind_speed_value

    def get_wind_dire(self):
        wind_dire = self.client.read_holding_registers(address=0x01f7, count=1)
        wind_dire_value = wind_dire.registers[0]

        return wind_dire_value #0°で北、時計回りに増えて90°で東を指す

    def get_atmos(self):
        atmos = self.client.read_holding_registers(address=0x01fd, count=1)
        atmos_value = atmos.registers[0]

        return atmos_value

    def get_rain(self):
        rain = self.client.read_holding_registers(address=0x0201, count=1)
        rain_value = rain.registers[0]/10

        return rain_value

    def close(self):
        self.client.close()
