from .. import device
import operator

import time

class sp100(device.device):
    manufacturer = 'COSMOTECHS'
    product_name = 'SP100'
    classification = 'Motor Controller'

    def command_set(self, unit, msg):
        target = bytes([32 + unit])
        self._send(target + msg)
        
        d1 = self._recv(1)
        if d1 != b'\x06':
            raise Exception(f'Bad response: {d1}')

        time.sleep(0.1)
        return
    
    def command_read(self, unit, msg):
        target = bytes([32 + unit])
        self._send(target + msg)
        
        d1 = self._recv(1)
        if d1 != b'\x06':
            raise Exception(f'Bad response: {d1}')
        
        d2 = self._readline()
        d3 = self._recv(2)
        bcc = self._calc_bcc(d2[1:-1])
        if d3.upper() != bcc:
            self._send(b'\x15')
            raise Exception(f'BCC not match: receieved = {d3}, calculated = {bcc}')
        
        self._send(b'\x06')
        return d2[4:-1].decode('ascii')
    
    def _send(self, msg):
        if type(msg) == str:
            msg = msg.encode()
            pass
        
        bcc = self._calc_bcc(msg)
        print(b'\x02'+msg+b'\x03'+bcc)
        return self.com.send(b'\x02'+msg+b'\x03'+bcc)

    def _recv(self, num):
        return self.com.recv(num).encode()
    
    def _readline(self):
        terminator = b'\x03'
        
        d = b''
        while True:
            _d = self._recv(1)
            d += _d
            if _d == terminator or _d == b'':
                break
            continue
        return d
        
    def _calc_bcc(self, d):
        tmp = 0
        for _ in d:
            tmp = operator.xor(tmp, _)
            continue
        return f'{tmp:02X}'.encode()
    
    
    # 30h
    # ---

    def origin_return_command(self, ax1=False, ax2=False, ax3=False, ax4=False, unit=0):
        command = b'\x30\x20'
        data = f'{ax1:d},{ax2:d},{ax3:d},{ax4:d}'
        
        return self.command_set(unit, command+data.encode())
    
    def absolute_move_command(self, ax1='', ax2='', ax3='', ax4='', unit=0):
        command = b'\x30\x22'
        data = ''

        if ax1 != '':
            data += f'{ax1:.3f},'
        else:
            data += ','
            pass
        
        if ax2 != '':
            data += f'{ax2:.3f},'
        else:
            data += ','
            pass
        
        if ax3 != '':
            data += f'{ax3:.3f},'
        else:
            data += ','
            pass
        
        if ax4 != '':
            data += f'{ax4:.3f}'
            pass
        
        return self.command_set(unit, command+data.encode())
    
    def immediately_stop_command(self, ax1=False, ax2=False, ax3=False, ax4=False, unit=0):
        command = b'\x30\x24'
        data = f'{ax1:d},{ax2:d},{ax3:d},{ax4:d}'
        
        return self.command_set(unit, command+data.encode())
    
    def decelerate_stop_command(self, ax1=False, ax2=False, ax3=False, ax4=False, unit=0):
        command = b'\x30\x25'
        data = f'{ax1:d},{ax2:d},{ax3:d},{ax4:d}'
        
        return self.command_set(unit, command+data.encode())

    def set_velocity_command(self, ax1=None, ax2=None, ax3=None, ax4=None, unit=0):
        command = b'\x30\x26'
        data = ''

        if ax1 is not None:
            data += f'{ax1:.3f},'
        else:
            data += ','
            pass
        
        if ax2 is not None:
            data += f'{ax2:.3f},'
        else:
            data += ','
            pass
        
        if ax3 is not None:
            data += f'{ax3:.3f},'
        else:
            data += ','
            pass
        
        if ax4 is not None:
            data += f'{ax4:.3f}'
            pass
        
        return self.command_set(unit, command+data.encode())

    def digital_output_query(self, unit=0):
        command = b'\x30\x28'
        
        d = self.command_read(unit, command)
        return [int(_) for _ in f"{int(d, base=16):032b}"[::-1]]
        
    def digital_output_command(self, port, status, unit=0):
        command = b'\x30\x28'
        data = f'{port:d},{status:d}'.encode()
        
        return self.command_set(unit, command+data)
        
    def control_status_query(self, unit=0):
        command = b'\x30\x2a'
        
        d = self.command_read(unit, command)
        bit = [int(_) for _ in f"{int(d, base=16):08b}"[::-1]]
        code = [
            'READY',
            'RUN',
            'ERROR',
            'SPO1',
            'BUSY-1',
            'BUSY-2',
            'BUSY-3',
            'BUSY-4',
        ]
        return {
            'code': d,
            'description': [code[i] for i,b in enumerate(bit) if b == 1],
        }
    
    # 40h
    # ---
    
    def current_positions_query(self, unit=0):
        command = b'\x40\x20'
        
        d = self.command_read(unit, command)
        return [float(_) for _ in d.split(',')]
        
    def axis_status_query(self, unit=0):
        command = b'\x40\x21'
        
        d = self.command_read(unit, command)
        dd = d.split(',')
        descriptions = {
            2**0: 'driving',
            2**1: 'positioning completed',
            2**2: '(NA)',
            2**3: '(NA)',
            2**4: 'origin return not completed',
            2**5: '(NA)',
            2**6: '(NA)',
            2**7: 'anomalous occurrence',
            2**8: 'software limit (+)',
            2**9: 'software limit (-)',
            2**10: 'limit senser (+)',
            2**11: 'limit senser (-)',
            2**12: '(NA)',
            2**13: '(NA)',
            2**14: '(NA)',
            2**15: 'alarm',
        }
        ret = []
        for i, code in enumerate(dd):
            ddd = {
                'code': code,
                'description': [descriptions[2**bit] for bit in range(16)
                                if int(code, base=16) & 2**bit],
            }

            if ddd['description'] == []:
                ddd['description'].append('no error')
                pass
            ret.append(ddd)
            continue

        return ret
            
    def axis_sensers_status_query(self, unit=0):
        command = b'\x40\x23'
        
        d = self.command_read(unit, command)
        dd = d.split(',')
        descriptions = {
            2**0: '+limit',
            2**1: '-limit',
            2**2: 'org',
            2**3: 'z',
            2**4: 'alarm',
            2**5: 'in position',
        }
        ret = []
        for i, code in enumerate(dd):
            ddd = {
                'code': code,
                'description': [descriptions[2**bit] for bit in range(6)
                                if int(code, base=16) & 2**bit],
            }

            if ddd['description'] == []:
                ddd['description'].append('no error')
                pass
            ret.append(ddd)
            continue

        return ret
            
    def error_code_query(self, unit=0):
        command = b'\x40\x24'
        
        d = self.command_read(unit, command)
        descriptions = {
            '00': 'no error',
            '01': '(NA)',
            '02': 'driving command error',
            '03': 'immediately stopped by emergency',
            '04': 'driver error',
            '05': 'program execution error',
            '06': 'origin return not completed',
            '07': 'limit error',
            '08': 'mode error',
            '09': 'positioning error',
            '10': 'command error',
            '11': 'data out of range',
            '12': 'format error',
            '13': 'command out of limit',
            '14': '(NA)',
            '15': '(NA)',
            '16': '(NA)',
            '17': 'normal error',
            '18': '(NA)',
            '19': '(NA)',
            '20': 'flush memory error',
        }
        return {
            'error_code': d,
            'description': descriptions[d],
        }

    def version_query(self, unit=0):
        command = b'\x40\x25'
        
        d = self.command_read(unit, command)
        dd = d.split(',')
        return {
            'version': dd[0],
            'timestamp': f'{dd[1]}-{dd[2]}-{dd[3]}',
        }

    def number_of_axes_query(self, unit=0):
        command = b'\x40\x26'
        
        d = self.command_read(unit, command)        
        descriptions = {
            '0': '2-axes',
            '1': '4-axes',
        }
        return {
            'code': d,
            'description': descriptions[d],
        }
    

    # 50h
    # ---
    
    def change_mode_query(self, unit=0):
        command = b'\x50\x2c'
        
        d = self.command_read(unit, command)
        descriptions = {
            '0': 'parameter',
            '1': 'manual',
            '2': 'position',
            '3': 'program',
            '4': 'auto',
            '5': 'remote',
            '6': 'monitor',
            '7': 'load',
            '8': 'save',
        }
        return {
            'mode': d,
            'description': descriptions[d],
        }
    
    def change_mode_command(self, mode, unit=0):
        command = b'\x50\x2c'
        mode = mode if type(bytes) == str else mode.encode()
        
        self.command_set(unit, command+mode)
        return self.change_mode_query(unit)

    
