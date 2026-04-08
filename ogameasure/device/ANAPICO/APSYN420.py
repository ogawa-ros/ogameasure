from __future__ import annotations

from ..SCPI import scpi
from ..communicator import ethernet

delay_time = 0.1


class APSYN420Error(RuntimeError):
    """Base exception for APSYN420 communication/control errors."""


class APSYN420ConnectionError(APSYN420Error):
    """Raised when connection/open/close fails."""


class APSYN420CommandError(APSYN420Error):
    """Raised when send/recv/query or device state validation fails."""


class InvalidRangeError(Exception):
    """Raised when the requested value is outside the supported range."""


class apsyn420(scpi.scpi_family):
    manufacturer = "ANAPICO"
    product_name = "APSYN420"
    classification = "Signal Generator"

    _scpi_enable = "*IDN? *RST"

    freq_range_ghz = (0.01, 20.0)
    power_default_dbm = 0.0
    power_range_dbm = (-20.0, 23.0)

    def __init__(self, host: str, port: int = 18, timeout: float = 1.0) -> None:
        self.host = host
        self.port = port
        self.timeout = timeout

        try:
            com = ethernet(host=host, port=port, timeout=timeout)
            com.open()
        except Exception as exc:
            raise APSYN420ConnectionError(
                f"Failed to connect to APSYN420 ({host}:{port})"
            ) from exc

        super().__init__(com)

    # --------------------
    # Internal helper
    # --------------------
    def _query(self, cmd: str) -> str:
        try:
            self.com.send(cmd)
            return self.com.readline().strip()
        except Exception as exc:
            raise APSYN420CommandError(
                f"Failed for command: {cmd}"
            ) from exc

    # --------------------
    # Basic ogameasure-style API
    # --------------------
    def freq_set(self, freq: float, unit: str = "GHz") -> None:
        self.com.send(f"FREQ:CW {freq:.10f} {unit}")

    def freq_query(self) -> float:
        return float(self._query("FREQ:CW?"))

    def power_set(self, power: float = 0.0) -> None:
        if not (self.power_range_dbm[0] <= power <= self.power_range_dbm[1]):
            msg = "Power range is {}[dBm] -- {}[dBm], while {}[dBm] is given.".format(
                self.power_range_dbm[0],
                self.power_range_dbm[1],
                power,
            )
            raise InvalidRangeError(msg)

        self.com.send(f"POW {power:f} dBm")

    def power_query(self) -> float:
        return float(self._query("POW?"))

    def output_on(self) -> None:
        self.com.send("OUTP ON")

    def output_off(self) -> None:
        self.com.send("OUTP OFF")

    def output_query(self) -> int:
        ret = self._query("OUTP?").upper()
        if ret in ("1", "ON"):
            return 1
        if ret in ("0", "OFF"):
            return 0
        raise APSYN420CommandError(f"Unexpected OUTP? response: {ret}")

    def close(self) -> None:
        try:
            self.com.close()
        except Exception as exc:
            raise APSYN420ConnectionError("Failed to close APSYN420 connection") from exc

    # --------------------
    # IEEE-488.2 common commands
    # --------------------
    def cls(self) -> None:
        self.com.send("*CLS")

    def ese_set(self, value: int) -> None:
        self.com.send(f"*ESE {int(value)}")

    def ese_query(self) -> int:
        return int(self._query("*ESE?"))

    def esr_query(self) -> int:
        return int(self._query("*ESR?"))

    def idn_query(self) -> str:
        return self._query("*IDN?")

    def opc(self) -> None:
        self.com.send("*OPC")

    def opc_query(self) -> int:
        return int(self._query("*OPC?"))

    def rst(self) -> None:
        self.com.send("*RST")

    def sre_set(self, value: int) -> None:
        self.com.send(f"*SRE {int(value)}")

    def sre_query(self) -> int:
        return int(self._query("*SRE?"))

    def stb_query(self) -> int:
        return int(self._query("*STB?"))

    def tst_query(self) -> int:
        return int(self._query("*TST?"))

    def wai(self) -> None:
        self.com.send("*WAI")

    # --------------------
    # Compatibility methods from your original APSYN420.py
    # --------------------
    def get_id(self) -> str:
        return self.idn_query()

    def get_ip(self) -> str:
        return self._query(':SYSTEM:COMMunicate:LAN:IP?').replace('"', "")

    def set_ip(self, ip: str) -> bool:
        if not isinstance(ip, str):
            raise APSYN420CommandError(
                "set_ip_01: IPv4 address must be given as a string."
            )

        self.com.send(f':SYSTem:COMMunicate:LAN:IP "{ip}"')
        res = self.get_ip()
        if ip != res:
            raise APSYN420CommandError(
                f"set_ip_02: Failed to set IPv4 address. Current IP = {res}"
            )
        return True

    def get_lan_mode(self) -> str:
        return self._query(":SYSTEM:COMMunicate:LAN:CONFig?")

    def set_lan_mode(self, mode: str = "DHCP") -> bool:
        self.com.send(f":SYSTEM:COMMunicate:LAN:CONFig {mode}")
        res = self.get_lan_mode()
        if mode != res:
            raise APSYN420CommandError(
                f"set_lan_mode_01: Failed to set LAN mode. Current mode = {res}"
            )
        return True

    def get_rf_onoff(self) -> str:
        return "ON" if self.output_query() == 1 else "OFF"

    def rf_on(self) -> bool:
        self.output_on()
        if self.get_rf_onoff() != "ON":
            raise APSYN420CommandError("RF could not be turned ON.")
        return True

    def rf_off(self) -> bool:
        self.output_off()
        if self.get_rf_onoff() != "OFF":
            raise APSYN420CommandError("RF could not be turned OFF.")
        return True

    def set_rf_mode(self, mode: str = "CW") -> bool:
        mode_list = ["CW", "FIXed", "SWEep", "LIST", "CHIRp"]
        if mode not in mode_list:
            raise APSYN420CommandError(
                'mode must be one of "CW", "FIXed", "SWEep", "LIST", "CHIRp".'
            )
        self.com.send(f":FREQuency:MODE {mode}")
        return True

    def get_rf_mode(self) -> str:
        return self._query(":FREQuency:MODE?")

    def get_freq(self) -> str:
        return self._query(":FREQuency?")

    def set_freq(self, freq: float = 1.0, unit: str = "GHz") -> bool:
        unit_scale = {
            "GHz": 1e9,
            "MHz": 1e6,
            "kHz": 1e3,
            "Hz": 1.0,
        }
        if unit not in unit_scale:
            raise APSYN420CommandError(
                'unit must be one of "GHz", "MHz", "kHz", "Hz".'
            )

        freq_hz = freq * unit_scale[unit]
        self.com.send(f":FREQuency {freq_hz:.3f}")
        res = float(self.get_freq())
        if freq_hz != res:
            print(
                f"[Caution] Actual frequency ({res:.3f} Hz) differs from requested "
                f"value ({freq_hz:.3f} Hz)."
            )
        return True

    def get_power(self) -> str:
        return self._query(":POWer?")

    def set_power(self, power: float = 1.0, unit: str = "dBm") -> bool:
        if unit != "dBm":
            raise APSYN420CommandError('unit must be "dBm".')
        self.com.send(f":POWer {power:f}")
        res = float(self.get_power())
        if power != res:
            print(
                f"[Caution] Actual power ({res:.3f} dBm) differs from requested "
                f"value ({power:.3f} dBm)."
            )
        return True

    def get_ref_ext_freq(self) -> str:
        return self._query(":ROSCillator:EXTernal:FREQuency?")

    def set_ref_ext_freq(self, ref_freq: float) -> bool:
        self.com.send(f":ROSCillator:EXTernal:FREQuency {ref_freq:.3f}")
        res = float(self.get_ref_ext_freq())
        if ref_freq != res:
            print(
                f"[Caution] Actual external reference frequency ({res:.3f} Hz) "
                f"differs from requested value ({ref_freq:.3f} Hz)."
            )
        return True

    def get_ref_locked(self) -> str:
        res = self._query(":ROSCillator:LOCKed?")
        if res == "0":
            return "OFF"
        if res == "1":
            return "ON"
        raise APSYN420CommandError(f"Unexpected ROSCillator:LOCKed? response: {res}")

    def get_ref_onoff(self) -> str:
        res = self._query(":ROSCillator:OUTPut?")
        if res == "0":
            return "OFF"
        if res == "1":
            return "ON"
        raise APSYN420CommandError(f"Unexpected ROSCillator:OUTPut? response: {res}")

    def ref_on(self) -> bool:
        self.com.send(":ROSCillator:OUTPut ON")
        if self.get_ref_onoff() != "ON":
            raise APSYN420CommandError("Reference output could not be turned ON.")
        return True

    def ref_off(self) -> bool:
        self.com.send(":ROSCillator:OUTPut OFF")
        if self.get_ref_onoff() != "OFF":
            raise APSYN420CommandError("Reference output could not be turned OFF.")
        return True

    def get_ref_selected(self) -> str:
        return self._query(":ROSCillator:SOURce?")

    def ref_internal(self) -> bool:
        self.com.send(":ROSCillator:SOURce INTernal")
        if self.get_ref_selected() != "INT":
            raise APSYN420CommandError("Failed to select internal reference.")
        return True

    def ref_external(self) -> bool:
        self.com.send(":ROSCillator:SOURce EXTernal")
        if self.get_ref_selected() != "EXT":
            raise APSYN420CommandError("Failed to select external reference.")
        return True

    def ref_slave(self) -> bool:
        self.com.send(":ROSCillator:SOURce SLAVe")
        if self.get_ref_selected() != "SLAV":
            raise APSYN420CommandError("Failed to select slave reference.")
        return True

    def reset(self) -> bool:
        self.rst()
        return True

    def __enter__(self) -> "apsyn420":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()