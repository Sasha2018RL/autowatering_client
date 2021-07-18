# import os
#
# import serial
#
#
# class SerialClient:
#     def __init__(self, socket_io_instance):
#         self.io = socket_io_instance
#         try:
#             ser = serial.Serial()
#             ser.port = "/dev/ttyUSB0"
#             ser.baudrate = 9600
#             ser.bytesize = serial.EIGHTBITS  # number of bits per bytes
#             ser.parity = serial.PARITY_NONE  # set parity check: no parity
#             ser.stopbits = serial.STOPBITS_ONE  # number of stop bits
#             # ser.timeout = None          #block read
#             ser.timeout = 1  # non-block read
#             # ser.timeout = 2              #timeout block read
#             ser.xonxoff = False  # disable software flow control
#             ser.rtscts = False  # disable hardware (RTS/CTS) flow control
#             ser.dsrdtr = False  # disable hardware (DSR/DTR) flow control
#             ser.writeTimeout = 2  # timeout for write
#             self.ser = ser
#         except Exception as e:
#             print(e)
#         self.io.emit('no-port', 'Успешно подключен к com порту')
#
#     def send(self, data):
#         print('written ' + data)
#         if not self.ser.isOpen():
#             self.ser.open()
#         self.ser.write(str.encode(data))
#
#     def poll(self):
#         pass
#         # seq = []
#         # count = 1
#         # joined_seq = ''
#         # for c in self.ser.read():
#         #     seq.append(chr(c))
#         #     joined_seq = ''.join(str(v) for v in seq)
#         #
#         #     if chr(c) == '\n':
#         #         print("Line " + str(count) + ': ' + joined_seq)
#         #         self.io.emit('uart-rx', joined_seq)
#         #         seq = []
#         #         count += 1
#         #         break
#         # return joined_seq
