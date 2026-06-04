#!/usr/bin/env python3

import time
import struct


class tr_702w_lan(object):

    SENSOR_ERROR_RAW = 0xEEEE

    def __init__(self, com, password: str = "password"):
        self.com = com
        self.password = password
        try:
            self.com.open()
            self.com.timeout = 5.0
            time.sleep(1.0)
            self.start()
        except Exception as e:
            print(f"Error during initialization: {e}")
            self.close()
            raise e

    def start(self):
        """Connect and authenticate via TCP socket."""
        self.com.recv()
        self.com.send(self.password + "\r")
        time.sleep(0.5)
        self.com.recv()

    # ------------------------------------------------------------------ #
    # Protocol helpers
    # ------------------------------------------------------------------ #

    def _build_cmd(self, cmd: bytes) -> bytes:
        """Wrap payload in T2 frame: b'T2' + LE-size + cmd + LE-checksum."""
        size = struct.pack("<H", len(cmd))
        checksum = struct.pack("<H", sum(cmd) & 0xFFFF)
        return b"T2" + size + cmd + checksum

    def _param_bytes(self, name: str, value) -> bytes:
        """Encode one parameter: NAME=<LE-2byte-size><ASCII-value>."""
        val = str(value).encode()
        return name.encode() + b"=" + struct.pack("<H", len(val)) + val

    def _parse_response(self, data: bytes, cmd_name: str) -> dict:
        """Sequentially decode all length-prefixed parameters in a response.

        Parameters are tightly packed: NAME=<LE-size><value>... with no
        separator, so we must walk forward by each declared size rather
        than searching for '='.
        """
        _VALID = frozenset(b"ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
        prefix = cmd_name.encode() + b":"
        start = data.find(prefix)
        if start == -1:
            return {}
        pos = start + len(prefix)
        params = {}
        while pos < len(data) - 3:
            eq = data.find(b"=", pos)
            if eq == -1:
                break
            name_b = data[pos:eq]
            if not name_b or len(name_b) > 8 or not all(c in _VALID for c in name_b):
                break
            if eq + 3 > len(data):
                break
            size = struct.unpack_from("<H", data, eq + 1)[0]
            val_start = eq + 3
            val_end = val_start + size
            if val_end > len(data):
                break
            params[name_b.decode()] = data[val_start:val_end]
            pos = val_end
        return params

    # ------------------------------------------------------------------ #
    # Connection management
    # ------------------------------------------------------------------ #

    def _reconnect(self):
        """Re-establish connection after link loss."""
        time.sleep(3.0)
        try:
            self.com.close()
        except Exception:
            pass
        self.com.open()
        self.start()

    def close(self):
        self.com.close()

    # ------------------------------------------------------------------ #
    # Measurement
    # ------------------------------------------------------------------ #

    def output_current_data(self) -> dict | None:
        """Return the latest temperature and humidity reading (ECRNT).

        Mirrors tr_73u.output_current_data() for a consistent API across devices.
        The device encodes raw values as (physical_value * 10) + 1000.
        CH1 = temperature (attribute 0x0D), CH2 = humidity (attribute 0xD0).

        Returns:
            dict with keys:
                temp_c : float  temperature in Celsius
                temp_k : float  temperature in Kelvin (absolute)
                humid  : float  relative humidity in %
            None if either channel reports a sensor error (0xEEEE).

        Raises:
            ConnectionResetError: if the device returns an empty response.
        """
        cmd = b"ECRNT:" + self._param_bytes("MODE", "0") + self._param_bytes("RANGE", "1")
        self.com.send_raw(self._build_cmd(cmd))
        time.sleep(0.5)
        data_raw = self.com.recv()

        if not data_raw:
            raise ConnectionResetError("Empty response from device")

        idx = data_raw.find(b"DATA=")
        if idx == -1:
            return None
        # Skip b"DATA=" (5 bytes) + 2-byte LE size field to reach the 0x40-byte header.
        hdr = data_raw[idx + 7:]

        # Offsets per spec: 0x20 = CH1 current value, 0x30 = CH2 current value
        ch1_raw = struct.unpack_from("<H", hdr, 0x20)[0]
        ch2_raw = struct.unpack_from("<H", hdr, 0x30)[0]

        if ch1_raw == self.SENSOR_ERROR_RAW or ch2_raw == self.SENSOR_ERROR_RAW:
            return None

        temp_c = (ch1_raw - 1000) / 10.0
        humid  = (ch2_raw - 1000) / 10.0
        return {
            "temp_c": temp_c,
            "temp_k": round(temp_c + 273.15, 2),
            "humid":  humid,
        }

    # ------------------------------------------------------------------ #
    # Device information & status
    # ------------------------------------------------------------------ #

    def get_device_info(self) -> dict:
        """Retrieve device identification parameters (RUINF).

        Returns:
            dict: {name, serial, fw_ver, net_ver}
        """
        self.com.send_raw(self._build_cmd(b"RUINF:"))
        time.sleep(0.5)
        p = self._parse_response(self.com.recv(), "RUINF")
        return {
            "name":    p.get("NAME",  b"").decode(errors="replace"),
            "serial":  p.get("SER",   b"").decode(errors="replace"),
            "fw_ver":  p.get("FWV",   b"").decode(errors="replace"),
            "net_ver": p.get("NETV",  b"").decode(errors="replace"),
        }

    def get_mac_address(self) -> str | None:
        """Retrieve the device MAC address (EBSTS).

        Returns:
            str: MAC address (e.g. "00:1A:2B:3C:4D:5E"), or None on failure.
        """
        status = self.get_status()
        return status.get("mac") or None

    def get_status(self) -> dict:
        """Retrieve device runtime status (EBSTS).

        Returns:
            dict: {ip, mac, state, ac}
                state: "initializing" | "running" | "error-stop" | "restart-required"
                ac:    "0" (no AC adapter) | "1" (AC adapter present)
        """
        _state_map = {
            b"0": "initializing", b"1": "running",
            b"2": "error-stop",   b"3": "restart-required",
        }
        self.com.send_raw(self._build_cmd(b"EBSTS:"))
        time.sleep(0.5)
        p = self._parse_response(self.com.recv(), "EBSTS")
        return {
            "ip":    p.get("IP",  b"").decode(),
            "mac":   p.get("MAC", b"").decode(),
            "state": _state_map.get(p.get("STATE"), "unknown"),
            "ac":    p.get("AC",  b"").decode(),
        }

    # ------------------------------------------------------------------ #
    # Webstorage (auto current-value transmission, WCURP)
    # ------------------------------------------------------------------ #

    def set_webstorage_interval(self, interval_min: int):
        """Set the auto current-value transmission interval (WCURP INT).

        Args:
            interval_min: Interval in minutes, 1-1440.
        """
        if not (1 <= interval_min <= 1440):
            raise ValueError(f"interval_min must be 1-1440, got {interval_min}")
        cmd = b"WCURP:" + self._param_bytes("INT", interval_min)
        self.com.send_raw(self._build_cmd(cmd))
        time.sleep(0.5)
        self.com.recv()

    def set_webstorage_enable(self, enable: bool):
        """Enable or disable auto current-value transmission (WCURP ENABLE).

        Args:
            enable: True to enable, False to disable.
        """
        cmd = b"WCURP:" + self._param_bytes("ENABLE", int(enable))
        self.com.send_raw(self._build_cmd(cmd))
        time.sleep(0.5)
        self.com.recv()

    def get_webstorage_settings(self) -> dict:
        """Read current auto current-value transmission settings (RCURP).

        Returns:
            dict: {enable, interval_min, route}
                route: "0" = E-Mail, "1" = FTP
        """
        self.com.send_raw(self._build_cmd(b"RCURP:"))
        time.sleep(0.5)
        p = self._parse_response(self.com.recv(), "RCURP")
        return {
            "enable":       p.get("ENABLE", b"0").decode(),
            "interval_min": p.get("INT",    b"60").decode(),
            "route":        p.get("ROUTE",  b"0").decode(),
        }

    # ------------------------------------------------------------------ #
    # Recording control
    # ------------------------------------------------------------------ #

    def start_recording(self, interval_sec: int = 60):
        """Start data logging immediately (EISET).

        Args:
            interval_sec: Recording interval in seconds.
                Valid values: 1/2/5/10/15/20/30/60/120/300/600/900/1200/1800/3600
        """
        cmd = (b"EISET:"
               + self._param_bytes("ACT",    "0")
               + self._param_bytes("INT",    interval_sec)
               + self._param_bytes("METHOD", "1"))
        self.com.send_raw(self._build_cmd(cmd))
        time.sleep(0.5)
        self.com.recv()

    def stop_recording(self):
        """Stop data logging (EIRSP)."""
        cmd = b"EIRSP:" + self._param_bytes("MODE", "1")
        self.com.send_raw(self._build_cmd(cmd))
        time.sleep(0.5)
        self.com.recv()

    # ------------------------------------------------------------------ #
    # Time & display settings
    # ------------------------------------------------------------------ #

    def time_sync(self):
        """Synchronize device clock to NTP via SNTP (WDTIM SYNC=2)."""
        cmd = b"WDTIM:" + self._param_bytes("SYNC", "2")
        self.com.send_raw(self._build_cmd(cmd))
        time.sleep(0.5)
        self.com.recv()

    def set_browse_time(self, interval_sec: int = 5):
        """Set WebViewer graph update interval in seconds (WWEBP INT, 5-60000)."""
        cmd = b"WWEBP:" + self._param_bytes("INT", interval_sec)
        self.com.send_raw(self._build_cmd(cmd))
        time.sleep(0.5)
        self.com.recv()
