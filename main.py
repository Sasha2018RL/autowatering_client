import sys

import socketio
import os
import threading
import time
from datetime import timedelta, datetime

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


@sio.on('en_watering')
def en_watering(watering_time):
    click(10, 3, int(watering_time), 60, True)


@sio.on('ds_watering')
def ds_watering():
    click(3)


@sio.on('hard_reset')
def hard_reset():
    reset()


@sio.on('en_usage')
def en_usage(usage_time):
    click(5, 4, int(usage_time), 600, True)


@sio.on('ds_usage')
def ds_usage():
    click(4)


def click(count, reset_count=0, timeout=0, max_time=60, reset_at_end=False):
    if timeout > max_time:
        timeout = max_time

    if timeout != 0:
        now = datetime.now()
        run_at = now + timedelta(minutes=timeout)
        delay = (run_at - now).total_seconds()

        threading.Timer(delay, click, [0, reset_count, 0, 1, reset_at_end]).start()
        os.system('bash /root/click.sh {}'.format(count))
    elif reset_at_end:
        reset()
    else:
        os.system('bash /root/click.sh {}'.format(reset_count))


def reset():
    os.system('bash /root/reset.sh')
    sio.emit('no-port', 'reset performed')


sio.connect('wss://sasha.hillel.it:8443/')
sio.emit('no-port', 'AWS Init done!')
reset()
