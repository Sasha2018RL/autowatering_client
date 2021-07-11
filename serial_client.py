import os

import serial


class SerialClient:
    def __init__(self, socket_io_instance):
        port_address = '/dev/ttyACM0'
        if not os.path.exists(port_address):
            port_address = '/dev/ttyUSB0'
            if not os.path.exists(port_address):
                port_address = '/dev/ttyUSB1'
        print(port_address)
        self.io = socket_io_instance
        self.ser = serial.Serial(
            port=port_address,
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=0)
        self.io.emit('no-port', 'Успешно подключен к порту '+port_address+'!')

    def send(self, data):
        print('written '+data)
        self.ser.write(str.encode(data))

    def poll(self):
        seq = []
        count = 1
        joined_seq = ''
        for c in self.ser.read():
            seq.append(chr(c))
            joined_seq = ''.join(str(v) for v in seq)

            if chr(c) == '\n':
                print("Line " + str(count) + ': ' + joined_seq)
                self.io.emit('uart-rx', joined_seq)
                seq = []
                count += 1
                break
        return joined_seq
