from __future__ import annotations

import math
import socket
import time
from typing import Optional


class APSYN420Error(RuntimeError):
    """Base exception for APSYN420 communication/control errors."""


class APSYN420ConnectionError(APSYN420Error):
    """Raised when connection/open/close fails."""


class APSYN420CommandError(APSYN420Error):
    """Raised when send/recv/query or device state validation fails."""


class APSYN420:
    def __init__(self, ip: str, port: int = 18, timeout: float = 1.0) -> None:
        self.ip = ip
        self.port = port
        self.timeout = timeout
        self.com: Optional[socket.socket] = None
        self.open()

    def open(self) -> bool:
        if self.com is not None:
            self.close()

        try:
            self.com = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.com.settimeout(self.timeout)
            self.com.connect((self.ip, self.port))
        except OSError as exc:
            self.com = None
            raise APSYN420ConnectionError("APSYN420_01: failed to connect") from exc
        return True

    def close(self) -> bool:
        if self.com is None:
            return True

        try:
            self.com.close()
        except OSError as exc:
            raise APSYN420ConnectionError("APSYN420_02: failed to close socket") from exc
        finally:
            self.com = None
        return True

    def _require_connection(self) -> socket.socket:
        if self.com is None:
            raise APSYN420ConnectionError("Socket is not connected.")
        return self.com

    def query(self, cmd: str) -> str:
        self.send(cmd)
        time.sleep(0.05)  # コマンド送信後、応答受信までの待ち時間
        return self.recv()

    def send(self, cmd: str) -> bool:
        sock = self._require_connection()
        try:
            sock.sendall(cmd.encode("utf-8"))
        except OSError as exc:
            raise APSYN420CommandError("APSYN420_03: failed to send command") from exc
        return True

    def recv(self, byte: int = 1024) -> str:
        sock = self._require_connection()
        try:
            recv = sock.recv(byte).decode("utf-8")
        except OSError as exc:
            raise APSYN420CommandError("APSYN420_04: failed to receive response") from exc
        return recv

    def get_id(self) -> str:
        cmd = "*IDN?\n"
        return self.query(cmd).rstrip("\n")

    def get_option(self) -> str:
        cmd = "*OPT?\n"
        res = self.query(cmd).split('"')
        if len(res) < 2:
            raise APSYN420CommandError("Failed to parse option response.")
        if res[1] == "0":
            return "None"
        if res[1] == "B3":
            return "Rechargeable Battery Pack"
        return "Complex"

    def show_id(self) -> bool:
        device_id = self.get_id()
        option = self.get_option()
        print(f"\n Device ID : {device_id}")
        print(f" Device Option : {option}\n")
        return True

    def get_ip(self) -> str:
        cmd = ':SYSTEM:COMMunicate:LAN:IP?\n'
        return self.query(cmd).replace('"', "").rstrip("\n")

    def show_ip(self) -> bool:
        res = self.get_ip()
        print(f"\n IPv4 Address = {res}\n")
        return True

    def set_ip(self, ip: str) -> bool:
        if not isinstance(ip, str):
            raise APSYN420CommandError(
                "set_IP_01: IPv4 Address は文字列で指定してください。例: '157.16.88.254'"
            )

        cmd = f':SYSTem:COMMunicate:LAN:IP "{ip}"\n'
        try:
            self.send(cmd)
            res = self.get_ip()
            if ip != res:
                raise APSYN420CommandError(
                    f"set_IP_02: 指定された IPv4 Address を設定出来ませんでした。現 IP = {res}"
                )
        except APSYN420Error:
            raise
        except Exception as exc:
            raise APSYN420CommandError(
                "set_IP_03: 指定された IPv4 Address を設定出来ませんでした。"
            ) from exc
        return True

    def get_lan_mode(self) -> str:
        cmd = ":SYSTEM:COMMunicate:LAN:CONFig?\n"
        return self.query(cmd).rstrip("\n")

    def show_lan_mode(self) -> bool:
        res = self.get_lan_mode()
        print(f"\n LAN IPv4 Mode = {res}\n")
        return True

    def set_lan_mode(self, mode: str = "DHCP") -> bool:
        cmd = f":SYSTEM:COMMunicate:LAN:CONFig {mode}\n"
        try:
            self.send(cmd)
            res = self.get_lan_mode()
            if mode != res:
                raise APSYN420CommandError(
                    f"set_LAN_mode_01: 指定された LAN IPv4 Mode を設定出来ませんでした。現 mode = {res}"
                )
        except APSYN420Error:
            raise
        except Exception as exc:
            raise APSYN420CommandError(
                "set_LAN_mode_02: 指定された LAN IPv4 Mode を設定出来ませんでした。"
            ) from exc
        return True

    def get_rf_onoff(self) -> str:
        cmd = ":OUTPut?\n"
        res = self.query(cmd).rstrip("\n")
        if res == "0":
            return "OFF"
        if res == "1":
            return "ON"
        raise APSYN420CommandError(
            "get_RF_onoff: RF の On/Off 状態を確認出来ませんでした。"
        )

    def show_rf(self) -> bool:
        onoff = self.get_rf_onoff()
        mode = self.get_rf_mode()
        if mode == "FIX":
            mode = "CW"
        print(f"\n RF Output : {onoff}")
        print(f" RF Output Mode : {mode}")
        self.show_freq()
        return True

    def rf_on(self) -> bool:
        cmd = ":OUTPut ON\n"
        res = self.send(cmd)
        if res:
            stat = self.get_rf_onoff()
            if stat == "ON":
                print(" > RF on clear")
            else:
                raise APSYN420CommandError(
                    "set_RF_on_01: RF を正常に On 状態に出来ませんでした。"
                )
        return res

    def rf_off(self) -> bool:
        cmd = ":OUTPut OFF\n"
        res = self.send(cmd)
        if res:
            stat = self.get_rf_onoff()
            if stat == "OFF":
                print(" > RF off clear")
            else:
                raise APSYN420CommandError(
                    "set_RF_on_01: RF を正常に Off 状態に出来ませんでした。"
                )
        return res

    def set_rf_mode(self, mode: str = "CW") -> bool:
        mode_list = ["CW", "FIXed", "SWEep", "LIST", "CHIRp"]
        if mode not in mode_list:
            raise APSYN420CommandError(
                'set_RF_mode_01: mode は "CW", "FIXed", "SWEep", "LIST", "CHIRp" のいずれかで指定してください。'
            )
        cmd = f":FREQuency:MODE {mode}\n"
        return self.send(cmd)

    def get_rf_mode(self) -> str:
        cmd = ":FREQuency:MODE?\n"
        return self.query(cmd).rstrip("\n")

    def show_rf_mode(self) -> bool:
        res = self.get_rf_mode()
        if res == "FIX":
            res = "CW"
        print(f"\n RF Output Mode : {res}\n")
        return True

    def get_freq(self) -> str:
        cmd = ":FREQuency?\n"
        return self.query(cmd)

    def show_freq(self) -> bool:
        freq = float(self.get_freq())
        if freq >= 5.0 * 10**8:
            print(f"\n Output Frequency = {freq / 10**9:.3f} [GHz]\n")
        elif 5.0 * 10**5 <= freq < 5.0 * 10**8:
            print(f"\n Output Frequency = {freq / 10**6:.3f} [MHz]\n")
        elif 5.0 * 10**2 <= freq < 5.0 * 10**5:
            print(f"\n Output Frequency = {freq / 10**3:.3f} [kHz]\n")
        elif freq < 5.0 * 10**2:
            print(f"\n Output Frequency = {freq:.3f} [Hz]\n")
        else:
            raise APSYN420CommandError(
                "show_freq_01: 有効な発振周波数を取得出来ませんでした。"
            )
        return True

    def show_freq_prec(self) -> bool:
        freq = float(self.get_freq())
        if freq >= 5.0 * 10**8:
            print(f"\n Output Frequency = {freq / 10**9:f} [GHz]\n")
        elif 5.0 * 10**5 <= freq < 5.0 * 10**8:
            print(f"\n Output Frequency = {freq / 10**6:f} [MHz]\n")
        elif 5.0 * 10**2 <= freq < 5.0 * 10**5:
            print(f"\n Output Frequency = {freq / 10**3:f} [kHz]\n")
        elif freq < 5.0 * 10**2:
            print(f"\n Output Frequency = {freq:f} [Hz]\n")
        else:
            raise APSYN420CommandError(
                "show_freq_01: 有効な発振周波数を取得出来ませんでした。"
            )
        return True

    def set_freq(self, freq: float = 1.0, unit: str = "GHz") -> bool:
        if unit == "GHz":
            freq_hz = freq * 10**9
        elif unit == "MHz":
            freq_hz = freq * 10**6
        elif unit == "kHz":
            freq_hz = freq * 10**3
        elif unit == "Hz":
            freq_hz = freq
        else:
            raise APSYN420CommandError(
                'set_freq_01: unit は "GHz", "MHz", "kHz", "Hz" のいずれかを指定してください。'
            )

        cmd = f":FREQuency {freq_hz:.3f}\n"
        self.send(cmd)
        res = float(self.get_freq())
        if freq_hz != res:
            print(f"\n [Caution] SG の発振周波数({res:.3f})と、設定値({freq_hz:.3f})が異なります。")
        return True

    def sweep_test1(self, start: float, stop: float, step: float, unit: str = "GHz") -> bool:
        point = math.ceil((stop - start) / step)
        i = 0
        while i <= point:
            freq = start + step * i
            self.set_freq(freq, unit)
            self.show_freq()
            i += 1
            if i < point:
                input("次の準備 OK ? : ")
        return True

    def get_power(self) -> str:
        cmd = ":POWer?\n"
        return self.query(cmd)

    def show_power(self) -> bool:
        power = float(self.get_power())
        if power >= -100:
            print(f"\n Output Power = {power:.3f} [dBm]\n")
        else:
            raise APSYN420CommandError(
                "show_power_01: 有効な発振パワーを取得出来ませんでした。"
            )
        return True

    def show_power_prec(self) -> bool:
        power = float(self.get_power())
        if power >= -100:
            print(f"\n Output Power = {power:f} [dBm]\n")
        else:
            raise APSYN420CommandError(
                "show_power_01: 有効な発振パワーを取得出来ませんでした。"
            )
        return True

    def set_power(self, power: float = 1.0, unit: str = "dBm") -> bool:
        if unit != "dBm":
            raise APSYN420CommandError(
                'set_power_01: unit は "dBm" を指定してください。'
            )
        cmd = f":POWer {power:f}\n"
        self.send(cmd)
        res = float(self.get_power())
        if power != res:
            print(f"\n [Caution] SG の発振パワー({res:.3f})と、設定値({power:.3f})が異なります。")
        return True

    def get_ref_ext_freq(self) -> str:
        cmd = ":ROSCillator:EXTernal:FREQuency?\n"
        return self.query(cmd)

    def set_ref_ext_freq(self, ref_freq: float) -> bool:
        cmd = f":ROSCillator:EXTernal:FREQuency {ref_freq:.3f}\n"
        self.send(cmd)
        res = float(self.get_ref_ext_freq())
        if ref_freq != res:
            print(
                f"\n [Caution] SG の外部リファレンス周波数({res:.3f})と、設定値({ref_freq:.3f})が異なります。"
            )
        return True

    def get_ref_locked(self) -> str:
        cmd = ":ROSCillator:LOCKed?\n"
        res = self.query(cmd).rstrip("\n")
        if res == "0":
            return "OFF"
        if res == "1":
            return "ON"
        raise APSYN420CommandError(
            "get_REF_onoff: リファレンス信号の状態を確認出来ませんでした。"
        )

    def get_ref_onoff(self) -> str:
        cmd = ":ROSCillator:OUTPut?\n"
        res = self.query(cmd).rstrip("\n")
        if res == "0":
            return "OFF"
        if res == "1":
            return "ON"
        raise APSYN420CommandError(
            "get_REF_onoff: リファレンス信号の ON/OFF 状態を確認出来ませんでした。"
        )

    def show_ref(self) -> bool:
        onoff = self.get_ref_onoff()

        # TODO:
        # 元コードでは get_REF_mode() が呼ばれているが、定義が存在しない。
        # 実機仕様が分かれば実装する。
        print(f"\n REF Output : {onoff}")
        return True

    def ref_on(self) -> bool:
        cmd = ":ROSCillator:OUTPut ON\n"
        res = self.send(cmd)
        if res:
            stat = self.get_ref_onoff()
            if stat == "ON":
                print(" > REF on clear")
            else:
                raise APSYN420CommandError(
                    "set_REF_on_01: リファレンス信号を正常に ON 状態に出来ませんでした。"
                )
        return res

    def ref_off(self) -> bool:
        cmd = ":ROSCillator:OUTPut OFF\n"
        res = self.send(cmd)
        if res:
            stat = self.get_ref_onoff()
            if stat == "OFF":
                print(" > REF off clear")
            else:
                raise APSYN420CommandError(
                    "set_REF_on_01: リファレンス信号を正常に OFF 状態に出来ませんでした。"
                )
        return res

    def get_ref_selected(self) -> str:
        cmd = ":ROSCillator:SOURce?\n"
        res = self.query(cmd).rstrip("\n")
        if res == "INT":
            print("\n リファレンスクロックは 内部の発振器 です。")
        elif res == "EXT":
            print("\n リファレンスクロックは 外部のクロック です。")
        elif res == "SLAV":
            print("\n リファレンスクロックは 100MHz固定の入力クロック です。")
        else:
            raise APSYN420CommandError(
                "get_REF_selected: リファレンス信号の状態を確認出来ませんでした。"
            )
        return res

    def ref_internal(self) -> bool:
        cmd = ":ROSCillator:SOURce INTernal\n"
        res = self.send(cmd)
        if res:
            stat = self.get_ref_selected()
            if stat == "INT":
                print(" > set REF INT")
            else:
                raise APSYN420CommandError(
                    "REF_internal: リファレンス信号を正常に選択できませんでした。"
                )
        return res

    def ref_external(self) -> bool:
        cmd = ":ROSCillator:SOURce EXTernal\n"
        res = self.send(cmd)
        if res:
            stat = self.get_ref_selected()
            if stat == "EXT":
                print(" > set REF EXT")
            else:
                raise APSYN420CommandError(
                    "REF_external: リファレンス信号を正常に選択できませんでした。"
                )
        return res

    def ref_slave(self) -> bool:
        cmd = ":ROSCillator:SOURce SLAVe\n"
        res = self.send(cmd)
        if res:
            stat = self.get_ref_selected()
            if stat == "SLAV":
                print(" > set REF SLAV")
            else:
                raise APSYN420CommandError(
                    "REF_slave: リファレンス信号を正常に選択できませんでした。"
                )
        return res

    def unit_power(self) -> None:
        # 元コードコメントに「このコマンド使えない」とあるため、挙動は維持
        cmd1 = ":UNIT:OUTPut DBUW"
        self.send(cmd1)
        cmd2 = ":UNIT:POWer?"
        self.send(cmd2)

    def reset(self) -> bool:
        cmd = "*RST\n"
        res = self.query(cmd).rstrip("\n")
        if res == "0":
            print("\n RF信号のON/OFF、周波数・パワー設定、外部リファレンス信号のON/OFFをリセットしました。")
        else:
            print("\n RF信号のON/OFF、周波数・パワー設定、外部リファレンス信号のON/OFFをリセット出来ませんでした。")
        return True

    def __enter__(self) -> "APSYN420":
        if self.com is None:
            self.open()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()