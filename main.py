import sys

from serial_client import SerialClient
import socketio
import os

# standard Python
sio = socketio.Client()


# sio.connect('ws://localhost:8080/')


@sio.event
def connect():
    print("I'm connected!")
    sio.emit('i-am-autowatering')


@sio.event
def connect_error(data):
    print("The connection failed!")


@sio.event
def disconnect():
    print("I'm disconnected!")


@sio.on('ping-q')
def ping():
    print('ping')
    sio.emit('ping-a')


@sio.on('reboot')
def reboot():
    print('rebooting')
    os.system('systemctl reboot -i')


@sio.on('restart')
def restart():
    print('restarting')
    sys.exit()


sio.connect('wss://sasha.hillel.it:8443/')

try:
    serial = SerialClient(socket_io_instance=sio)


    @sio.on('uart-tx-stage2')
    def uart_rx(data):
        serial.send(data)

    serial.poll()
except Exception as e:
    print(e)
    sio.emit('no-port', str(e))