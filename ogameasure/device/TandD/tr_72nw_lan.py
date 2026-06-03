#!/usr/bin/env python3

import struct


class tr_72nw_lan(object):
    """TR-7nw (TR-72NW) LAN リモートコントロールドライバ。

    通信方式:
      - ポート 57172 固定、認証なし
      - TR-7nw はコマンド応答後にセッションを切断するため、
        コマンドごとに TCP 接続を open → send → recv → close する
      - コマンドフレーム:
          SerialNo(4,LE) + CmdSize(2,LE)
          + SOH(0x01) + Cmd(1) + SubCmd(0x00) + DataLen(2,LE) + Data + SUM(2,LE)
      - 応答フレーム (1064byte 固定受信、先頭の実データのみ使用):
          SOH(0x01) + Cmd(1) + RespCode(1) + DataLen(2,LE) + Data + SUM(2,LE)
          RespCode: 0x06=正常 / 0x09=記録中
    """

    PORT      = 57172
    RESP_SIZE = 1064
    ACK       = 0x06

    # 動作設定 64byte 書き込み/読み出し (0x6C/0x6D) のアドレス
    _ADDR_WF_EV  = 0x00C0   # 自動送信設定テーブル (WF_EV)
    _ADDR_WF_ALM = 0x0380   # 警報設定テーブル    (WF_ALM)

    def __init__(self, com, serial_no: int):
        """
        Args:
            com       : 通信オブジェクト (port=57172 のホストに接続するもの)
            serial_no : 機器のシリアル番号 (10進整数)
                        例: シリアル番号 "5214ABCD" (16進) → int("5214ABCD", 16)
        """
        self.com = com
        self.serial_no = serial_no
        self.com.timeout = 5.0

    def start(self):
        """互換性のために残す。TR-7nw はログイン不要。"""
        pass

    # ------------------------------------------------------------------ #
    # Protocol helpers
    # ------------------------------------------------------------------ #

    def _build_cmd(self, command: int, data: bytes = b"\x00\x00\x00\x00") -> bytes:
        """T&D バイナリコマンドフレームを組み立てる。

        CommandBody = SOH + Cmd + SubCmd(0x00) + DataLen(2,LE) + Data + SUM(2,LE)
        SUM = SOH から Data 末尾までを 1byte ごとに加算した値の下位 16bit (LE)
        """
        body = (bytes([0x01, command, 0x00])
                + struct.pack("<H", len(data))
                + data)
        checksum = struct.pack("<H", sum(body) & 0xFFFF)
        body += checksum
        serial_b = struct.pack("<I", self.serial_no)
        return serial_b + struct.pack("<H", len(body)) + body

    def _parse_response(self, raw: bytes) -> tuple[bool, bytes]:
        """1064byte 応答フレームを解析して (成功フラグ, ペイロード) を返す。"""
        if len(raw) < 5:
            return False, b""
        resp_code = raw[2]
        data_len  = struct.unpack_from("<H", raw, 3)[0]
        payload   = raw[5 : 5 + data_len]
        return resp_code == self.ACK, payload

    def _query(self, command: int, data: bytes = b"\x00\x00\x00\x00") -> tuple[bool, bytes]:
        """コマンドを送信して応答を受信する。

        TR-7nw は応答後にセッションを切断するため、毎回 open/close する。
        """
        self.com.open()
        try:
            self.com.send_raw(self._build_cmd(command, data))
            raw = self.com.recv()
            return self._parse_response(raw)
        finally:
            try:
                self.com.close()
            except Exception:
                pass

    # ------------------------------------------------------------------ #
    # Measurement  (tr_73u / tr_702w_lan 互換)
    # ------------------------------------------------------------------ #

    def output_current_data(self) -> dict | None:
        """現在値読み取り (コマンド 0x33)。

        TR-72nw: CH1=温度、CH2=湿度
        生データ変換式: (raw - 1000) / 10

        Returns:
            dict:
                temp_c : float  温度 [°C]
                temp_k : float  温度 [K] (絶対温度)
                humid  : float  相対湿度 [%RH]
            None on failure.
        """
        ok, payload = self._query(0x33)
        if not ok or len(payload) < 4:
            return None

        ch1_raw = struct.unpack_from("<H", payload, 0)[0]
        ch2_raw = struct.unpack_from("<H", payload, 2)[0]

        temp_c = (ch1_raw - 1000) / 10.0
        humid  = (ch2_raw - 1000) / 10.0
        return {
            "temp_c": temp_c,
            "temp_k": round(temp_c + 273.15, 2),
            "humid":  humid,
        }

    # ------------------------------------------------------------------ #
    # Device information
    # ------------------------------------------------------------------ #

    def get_device_info(self) -> dict:
        """機種名・機種コード・シリアル番号を取得する。

        Returns:
            dict:
                name         : str  機種名 ASCII (例: "TR-72nw")
                serial       : int  シリアル番号
                machine_code : int  0x0498=TR-71nw / 0x0499=TR-72nw / 0x0807=TR-75nw
        """
        _, name_pl   = self._query(0x36)   # 機種名
        _, code_pl   = self._query(0x35)   # 機種コード
        _, serial_pl = self._query(0x58)   # シリアル番号

        name  = name_pl[:7].rstrip(b"\x00").decode("ascii", errors="replace") if name_pl else ""
        mcode = struct.unpack_from("<H", code_pl,   0)[0] if len(code_pl)   >= 2 else 0
        ser   = struct.unpack_from("<I", serial_pl, 0)[0] if len(serial_pl) >= 4 else 0
        return {
            "name":         name,
            "serial":       ser,
            "machine_code": mcode,
        }

    def get_firmware_version(self) -> float | None:
        """ファームウェアバージョン取得 (0x72)。

        Returns:
            float バージョン (例: 2.01)、失敗時 None
        """
        ok, payload = self._query(0x72)
        if not ok or len(payload) < 1:
            return None
        return payload[0] / 100.0

    def get_battery_voltage(self) -> dict | None:
        """電池電圧取得 (0x39)。

        Returns:
            dict: {voltage_v: float, level: int (0-5)}
        """
        ok, payload = self._query(0x39)
        if not ok or len(payload) < 3:
            return None
        return {
            "voltage_v": struct.unpack_from("<H", payload, 0)[0] / 100.0,
            "level":     payload[2],
        }

    def get_mac_address(self) -> str | None:
        """MAC アドレス取得 (0x6E)。"""
        ok, payload = self._query(0x6E)
        if not ok or len(payload) < 6:
            return None
        return ":".join(f"{b:02X}" for b in payload[:6])

    def get_record_count(self) -> int | None:
        """記録データ数取得 (0x34)。"""
        ok, payload = self._query(0x34)
        if not ok or len(payload) < 2:
            return None
        return struct.unpack_from("<H", payload, 0)[0]

    # ------------------------------------------------------------------ #
    # 動作設定 64byte 読み書き (0x6D / 0x6C)
    # ------------------------------------------------------------------ #

    def _read_settings_64(self, address: int) -> bytes | None:
        """動作設定の 64byte ブロックを読み出す (0x6D)。

        Args:
            address: 0x00C0 (WF_EV) または 0x0380 (WF_ALM)
        Returns:
            64 bytes の設定データ、失敗時 None
        """
        data = struct.pack("<H", address) + b"\x00\x00"
        ok, payload = self._query(0x6D, data)
        if not ok or len(payload) < 66:
            return None
        return bytes(payload[2:66])   # 先頭 2 bytes はアドレスのエコー

    def _write_settings_64(self, address: int, settings: bytes) -> bool:
        """動作設定の 64byte ブロックを書き込む (0x6C)。

        Args:
            address : 0x00C0 (WF_EV) または 0x0380 (WF_ALM)
            settings: 64 bytes の設定データ
        Returns:
            True on success.
        """
        if len(settings) != 64:
            raise ValueError(f"settings must be 64 bytes, got {len(settings)}")
        data = struct.pack("<H", address) + settings
        ok, _ = self._query(0x6C, data)
        return ok

    # ------------------------------------------------------------------ #
    # Webstorage (自動送信設定、WF_EV テーブル)
    # ------------------------------------------------------------------ #

    def set_webstorage_interval(self, interval_sec: int) -> bool:
        """自動送信間隔を設定する (WF_EV テーブル)。

        WF_EV テーブル (アドレス 0x00C0):
          Adr.0   : 自動送信 ON/OFF (0=OFF / 1=ON)
          Adr.4-7 : 自動送信間隔 [秒] (DWORD, LE)

        現在値を読み出してから指定フィールドのみ変更して書き戻す。

        Args:
            interval_sec: 送信間隔 [秒]。0 を指定すると自動送信 OFF。
        Returns:
            True on success.
        """
        table = self._read_settings_64(self._ADDR_WF_EV)
        if table is None:
            return False
        table = bytearray(table)
        table[0] = 1 if interval_sec > 0 else 0
        struct.pack_into("<I", table, 4, interval_sec)
        return self._write_settings_64(self._ADDR_WF_EV, bytes(table))

    def set_webstorage_enable(self, enable: bool) -> bool:
        """自動送信の ON/OFF のみ切り替える (WF_EV テーブル)。"""
        table = self._read_settings_64(self._ADDR_WF_EV)
        if table is None:
            return False
        table = bytearray(table)
        table[0] = 1 if enable else 0
        return self._write_settings_64(self._ADDR_WF_EV, bytes(table))

    def get_webstorage_settings(self) -> dict | None:
        """現在の自動送信設定を取得する (WF_EV テーブル)。

        Returns:
            dict: {enable: bool, interval_sec: int}
        """
        table = self._read_settings_64(self._ADDR_WF_EV)
        if table is None:
            return None
        return {
            "enable":       bool(table[0]),
            "interval_sec": struct.unpack_from("<I", table, 4)[0],
        }

    # ------------------------------------------------------------------ #
    # Recording control
    # ------------------------------------------------------------------ #

    def start_recording(self, interval_sec: int = 60) -> bool:
        """記録設定 & 記録開始 (0x3D)。

        Args:
            interval_sec: 記録間隔 [秒]
                有効値: 1/2/5/10/15/20/30/60/120/300/600/900/1200/1800/3600
        Returns:
            True on success.
        """
        table = bytearray(64)
        struct.pack_into("<H", table, 0, interval_sec)  # 記録間隔 (Adr.0-1)
        table[42] = 0x00   # 記録開始状態: 0=即時
        table[43] = 0x00   # 記録モード: 0x00=エンドレス
        ok, _ = self._query(0x3D, bytes(table))
        return ok

    def stop_recording(self) -> bool:
        """記録解除 (0x32)。

        Returns:
            True on success.
        """
        ok, _ = self._query(0x32)
        return ok

    # ------------------------------------------------------------------ #
    # Compatibility / cleanup
    # ------------------------------------------------------------------ #

    def close(self):
        """互換性のために残す。接続はコマンドごとに自動管理される。"""
        try:
            self.com.close()
        except Exception:
            pass
