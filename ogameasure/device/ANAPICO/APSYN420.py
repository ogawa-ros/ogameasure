from __future__ import annotations

from ..SCPI import scpi

delay_time = 0.1


class APSYN420Error(RuntimeError):
    """Base exception for APSYN420 control errors."""


class APSYN420CommandError(APSYN420Error):
    """Raised when a command fails or a device state is invalid."""


class InvalidRangeError(Exception):
    """Raised when the requested value is outside the supported range."""


class APSYN420(scpi.scpi_family):
    manufacturer = "ANAPICO"
    product_name = "APSYN420"
    classification = "Signal Generator"

    _scpi_enable = "*IDN? *RST"

    freq_range_ghz = (0.01, 20.0)
    power_default_dbm = 0.0
    power_range_dbm = (-20.0, 23.0)

    def _query(self, cmd: str) -> str:
        try:
            self.com.send(cmd)
            return self.com.readline().rstrip("\n")
        except Exception as exc:
            raise APSYN420CommandError(f"Failed for command: {cmd}") from exc

    # ============================================================
    # ogameasure standard API
    # ============================================================
    def freq_set(self, freq: float, unit: str = "GHz") -> None:
        """
        Set CW output frequency.

        Parameters
        ----------
        freq : float
            Frequency value.
        unit : str, default "GHz"
            Unit of frequency. One of "GHz", "MHz", "kHz", or "Hz".
        """
        if unit == "GHz":
            freq_hz = freq * 1e9
        elif unit == "MHz":
            freq_hz = freq * 1e6
        elif unit == "kHz":
            freq_hz = freq * 1e3
        elif unit == "Hz":
            freq_hz = freq
        else:
            raise APSYN420CommandError(
                'unit must be one of "GHz", "MHz", "kHz", or "Hz".'
            )

        self.com.send(":FREQuency %.3f" % freq_hz)

    def freq_query(self) -> float:
        """
        Query CW output frequency in Hz.

        Returns
        -------
        float
            Output frequency in Hz.
        """
        return float(self._query(":FREQuency?"))

    def power_set(self, power: float = 0.0) -> None:
        """
        Set output power in dBm.

        Parameters
        ----------
        power : float, default 0.0
            Output power in dBm.
        """
        if not (self.power_range_dbm[0] <= power <= self.power_range_dbm[1]):
            msg = "Power range is {}[dBm] -- {}[dBm], while {}[dBm] is given.".format(
                self.power_range_dbm[0],
                self.power_range_dbm[1],
                power,
            )
            raise InvalidRangeError(msg)

        self.com.send(":POWer %f" % power)

    def power_query(self) -> float:
        """
        Query output power in dBm.

        Returns
        -------
        float
            Output power in dBm.
        """
        return float(self._query(":POWer?"))

    def output_on(self) -> None:
        """Turn RF output on."""
        self.com.send(":OUTPut ON")

    def output_off(self) -> None:
        """Turn RF output off."""
        self.com.send(":OUTPut OFF")

    def output_query(self) -> int:
        """
        Query RF output state.

        Returns
        -------
        int
            1 if RF output is ON, 0 if OFF.
        """
        ret = self._query(":OUTPut?")
        if ret == "1":
            return 1
        if ret == "0":
            return 0
        raise APSYN420CommandError(f"Unexpected OUTPut? response: {ret}")

    def close(self) -> None:
        """Close communicator."""
        self.com.close()

    # ============================================================
    # IEEE-488.2 common commands
    # ============================================================
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

    # ============================================================
    # Optional APSYN420-specific helper methods
    # ============================================================
    def lan_ip_query(self) -> str:
        return self._query(":SYSTEM:COMMunicate:LAN:IP?").replace('"', "")

    def lan_ip_set(self, ip: str) -> None:
        if not isinstance(ip, str):
            raise APSYN420CommandError("IP address must be given as a string.")
        self.com.send(':SYSTem:COMMunicate:LAN:IP "%s"' % ip)

    def lan_mode_query(self) -> str:
        return self._query(":SYSTEM:COMMunicate:LAN:CONFig?")

    def lan_mode_set(self, mode: str = "DHCP") -> None:
        self.com.send(":SYSTEM:COMMunicate:LAN:CONFig %s" % mode)

    def rf_mode_set(self, mode: str = "CW") -> None:
        mode_list = ["CW", "FIXed", "SWEep", "LIST", "CHIRp"]
        if mode not in mode_list:
            raise APSYN420CommandError(
                'mode must be one of "CW", "FIXed", "SWEep", "LIST", or "CHIRp".'
            )
        self.com.send(":FREQuency:MODE %s" % mode)

    def rf_mode_query(self) -> str:
        return self._query(":FREQuency:MODE?")

    def ref_ext_freq_set(self, ref_freq: float) -> None:
        self.com.send(":ROSCillator:EXTernal:FREQuency %.3f" % ref_freq)

    def ref_ext_freq_query(self) -> float:
        return float(self._query(":ROSCillator:EXTernal:FREQuency?"))

    def ref_locked_query(self) -> int:
        ret = self._query(":ROSCillator:LOCKed?")
        if ret == "1":
            return 1
        if ret == "0":
            return 0
        raise APSYN420CommandError(f"Unexpected ROSCillator:LOCKed? response: {ret}")

    def ref_output_on(self) -> None:
        self.com.send(":ROSCillator:OUTPut ON")

    def ref_output_off(self) -> None:
        self.com.send(":ROSCillator:OUTPut OFF")

    def ref_output_query(self) -> int:
        ret = self._query(":ROSCillator:OUTPut?")
        if ret == "1":
            return 1
        if ret == "0":
            return 0
        raise APSYN420CommandError(f"Unexpected ROSCillator:OUTPut? response: {ret}")

    def ref_source_set(self, source: str) -> None:
        allowed = {
            "INT": "INTernal",
            "EXT": "EXTernal",
            "SLAV": "SLAVe",
        }
        if source not in allowed:
            raise APSYN420CommandError(
                'source must be one of "INT", "EXT", or "SLAV".'
            )
        self.com.send(":ROSCillator:SOURce %s" % allowed[source])

    def ref_source_query(self) -> str:
        ret = self._query(":ROSCillator:SOURce?")
        if ret not in ("INT", "EXT", "SLAV"):
            raise APSYN420CommandError(f"Unexpected ROSCillator:SOURce? response: {ret}")
        return ret

    def reset(self) -> None:
        self.com.send("*RST")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()