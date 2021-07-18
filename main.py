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
    sio.emit('no-port', 'Включаю полив')
    click(10, 3, int(watering_time), 60, True)
    sio.emit('no-port', 'Включен полив на {} минут'.format(watering_time))


@sio.on('ds_watering')
def ds_watering():
    sio.emit('no-port', 'Отключаю полив')
    click(4)
    sio.emit('no-port', 'Полив отключен')


@sio.on('hard_reset')
def hard_reset():
    sio.emit('no-port', 'Сбрасываю')
    reset()


@sio.on('en_usage')
def en_usage(usage_time):
    sio.emit('no-port', 'Включаю использование')
    click(5, 4, int(usage_time), 600, True)
    sio.emit('no-port', 'Включено использование на {} минут'.format(usage_time))


@sio.on('ds_usage')
def ds_usage():
    sio.emit('no-port', 'Отключаю использование')
    click(3)
    sio.emit('no-port', 'Использование отключено')


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
    sio.emit('no-port', 'Arduino перезапущена!')


sio.connect('wss://sasha.hillel.it:8443/')
sio.emit('no-port', 'AWS Init done!')
reset()
