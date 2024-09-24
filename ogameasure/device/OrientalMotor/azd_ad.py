from .. import device
import time


class azd_ad(device.device):
    manufacturer = "OrientalMotor"
    product_name = "AZD-AD"
    classification = "Motor Controller"

    def initialize(self):
        self.zero_return()
        self.alarm_reset()
        self.alarm_clear()
        return

    def zero_return(self):
        """
        first zero returning operation

        Parameters
        ----------

        """
        start_command = create_query("0106007D0010")
        self.com.send_raw(start_command)
        time.sleep(1)
        _ = self.com.recv()
        end_command = create_query("0106007D0000")
        self.com.send_raw(end_command)
        time.sleep(0.05)
        _ = self.com.recv()
        return

    def direct_operation(self, location=11000, speed=80000, acc=1000000):
        """
        direct operation

        Parameters
        ----------
        location : int
        step

        speed : int
        speed

        acc : int
        acceleration

        """
        speed_hex = format(speed, "08x")
        location_hex = format(location, "08x")
        acc_hex = format(acc, "08x")
        command = create_query(
            "01 10 0058 0010 20 00000000 00000001"
            + location_hex
            + speed_hex
            + acc_hex
            + acc_hex
            + "000003E8 00000001"
        )
        self.com.send_raw(command)
        time.sleep(0.05)
        _ = self.com.recv()
        return

    def get_current_position(self):
        position_command = create_query("010300CC0002")
        self.com.send_raw(position_command)
        time.sleep(0.05)
        msg = self.com.recv().hex()
        position = int(msg[10:14], 16)
        return position

    def alarm_query(self):
        query_command = create_query("010300800002")
        self.com.send_raw(query_command)
        time.sleep(0.05)
        msg = self.com.recv().hex()
        alarm_code = msg[10:14]
        return alarm_code

    def alarm_reset(self):
        reset_command = create_query("0110018000020400000000")
        self.com.send_raw(reset_command)
        time.sleep(0.05)
        _ = self.com.recv().hex()
        reset_command = create_query("0110018000020400000001")
        self.com.send_raw(reset_command)
        time.sleep(0.05)
        _ = self.com.recv().hex()
        return

    def alarm_clear(self):
        clear_command = create_query("0110018400020400000000")
        self.com.send_raw(clear_command)
        time.sleep(0.05)
        _ = self.com.recv().hex()
        clear_command = create_query("0110018400020400000001")
        self.com.send_raw(clear_command)
        time.sleep(0.05)
        _ = self.com.recv().hex()
        return


def crc16(command):
    """
    crc-16 error check

    Parameters
    ----------
    command : bytes

    Returns
    -------
    crc : bytes

    """

    crc_register = 0xFFFF
    for data_byte in command:
        crc_register ^= data_byte
        for _ in range(8):
            overflow = crc_register & 1 == 1
            crc_register >>= 1
            if overflow:
                crc_register ^= 0xA001

    crc = crc_register.to_bytes(2, "little")
    return crc


def create_query(hex_command):
    """

    Parameters
    ----------
    hex_command : char

    Returns
    -------
    query : bytes

    """
    bytes_command = bytes.fromhex(hex_command)
    error_check = crc16(bytes_command)
    query = bytes_command + error_check
    return query
