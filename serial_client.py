import os

import serial


class SerialClient:
    def __init__(self, socket_io_instance):
        self.io = socket_io_instance
        try:
            self.ser = serial.Serial(
                port='/dev/ttyUSB0',
                baudrate=9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=0)
        except Exception as e:
            print(e)
            try:
                self.ser = serial.Serial(
                    port='/dev/ttyACM0',
                    baudrate=9600,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                    timeout=0)
                return
            except Exception as e:
                print(e)
                self.ser = serial.Serial(
                    port='/dev/ttyUSB1',
                    baudrate=9600,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                    timeout=0)
        self.io.emit('no-port', 'Успешно подключен к com порту')

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
