from .. import device

class tpg261(device.device):
    manufacturer = 'Pfeiffer Vacuum'
    product_name = 'TPG261'
    classification = 'Vacuum Gauge'

    def _command(self, cmd):
        self.com.send(cmd)
        self._check_response()
        return

    def _query(self, cmd):
        self.com.send(cmd)
        self._check_response()
        self.com.send('\x05')
        d = self.com.readline().strip()
        if d.find(',') != -1: return d.split(',')
        return d
    
    def _check_response(self):
        res = self.com.readline().strip()
        if res == '\x06':
            return
        elif res == '\x15':
            self.com.send('\x05')
            error_no = self.com.readline().strip()
            error_msgs = []
            if error_no[0] == '1': error_msgs.append('Controller error')
            if error_no[1] == '1': error_msgs.append('No hardware')
            if error_no[2] == '1': error_msgs.append('Inadmissible parameter')
            if error_no[3] == '1': error_msgs.append('Syntax error')
            raise Exception(f'Error: error_code = {error_no}, msg = {error_msgs}.')
        
        raise Exception(f'Error: unexpected response. res = {res}.')
    
    def read_single_pressure(self, ch=1):
        d = self._query(f'PR{ch}')
        return self._decode_pr_reply(d[0], d[1])

    def read_pressure(self):
        d = self._query('PRX')
        return {
            'ch1': self._decode_pr_reply(d[0], d[1]),
            'ch2': self._decode_pr_reply(d[2], d[3]),
        }

    def _decode_pr_reply(self, d0, d1):
        status_msg = {
            '0': 'OK',
            '1': 'Underrange',
            '2': 'Overrange',
            '3': 'Sensor error',
            '4': 'Sensor off',
            '5': 'No sensor',
            '6': 'Identification error',
        }
        
        return {
            'status_code': int(d0),
            'status': status_msg[d0],
            'value': float(d1),
        }

    def start_continuous_output(self, mode=1):
        self._command(f'COM,{mode}')
        return
    
    def wait_and_receive_pressure_output(self):
        d = self.com.readline().strip().split(',')
        return {
            'ch1': self._decode_pr_reply(d[0], d[1]),
            'ch2': self._decode_pr_reply(d[2], d[3]),
        }

    def stop_continous_output(self):
        self.com.send('\x05')
        self.com.recv(1000000)
        return
    
    def gauge_status_query(self):
        return self.gauge_status_command()

    def gauge_status_command(self, ch1=0, ch2=0):
        d = self._query(f'SEN,{ch1},{ch2}')
        
        status_msg = {
            '0': 'unavailable',
            '1': 'off',
            '2': 'on',
        }
        return {
            'ch1': {
                'code': int(d[0]),
                'message': status_msg[d[0]],
            },
            'ch2': {
                'code': int(d[1]),
                'message': status_msg[d[1]],
            },
        }
    
    def gauge_identification_query(self):
        d = self._query('TID')

        id_msg = {
            'TPR': 'Pirani Gauge',
            'IKR9': 'Cold Cathode Gauge 1e-9',
            'IKR11': 'Cold Cathode Gauge 1e-11',
            'PKR': 'FullRange CC Gauge',
            'PBR': 'FullRange BA Gauge',
            'IMR': 'Pirani / High Pressure Gauge',
            'CMR': 'Linear gauge',
            'noSen': 'no Sensor',
            'noid': 'no identifier',
        }
        return {
            'ch1': {
                'id': d[0],
                'description': id_msg[d[0]],
            },
            'ch2': {
                'id': d[1],
                'description': id_msg[d[1]],
            }
        }

    def display_channel_command(self, ch=None):
        if ch is None:
            d = self._query('SCT')
        else:
            d = self._query(f'SCT,{ch}')
            pass
        
        display_msg = {
            '0': 'Gauge 1',
            '1': 'Gauge 2',
        }
        return {
            'code': int(d),
            'description': display_msg[d],
        }

    def display_channel_query(self):
        return self.display_channel_command()

    def reset_error_command(self):
        d = self._query('RES,1')
        return self._decode_res(d)
        
    def error_query(self):
        d = self._query('RES')
        return self._decode_res(d)

    def _decode_res(self, errors):
        msg = {
            '0': 'No error',
            '1': 'Watchdog has responded',
            '2': 'Task fail error',
            '3': 'EPROM error',
            '4': 'RAM error',
            '5': 'EEPROM error',
            '6': 'Display error',
            '7': 'A/D converter error',
            '8': '',
            '9': 'Gauge 1 error (e.g., filament rupture, no supply)',
            '10': 'Gauge 1 identification error',
            '11': 'Gauge 2 error (e.g., filament rupture, no supply)',
            '12': 'Gauge 2 identification error',
        }

        ret = []
        for e in errors.split(','):
            ret.append({
                'code': int(e),
                'message': msg[e],
            })
            continue
        return ret

    def unit_query(self):
        return self.unit_command()

    def unit_command(self, unit=None):
        if unit is None:
            d = self._query('UNI')
        else:
            d = self._query(f'UNI,{unit}')
            pass
        
        desc = {
            '0': 'mbar/bar',
            '1': 'Torr',
            '2': 'Pascal',
        }
        return {
            'code': int(d),
            'unit': desc[d],
        }

    def display_resolution_query(self):
        return self.display_resolution_command()
    
    def display_resolution_command(self, res=None):
        if res is None:
            d = self._query('DCD')
        else:
            d = self._query(f'DCD,{res}')
            pass

        desc = {
            '2': 'Display x.x (2 digits)',
            '3': 'Display x.xx (3 digits)',
        }
        return {
            'code': int(d),
            'description': desc[d],
        }

    def firmware_version_query(self):
        return self._query('PNR')
    
