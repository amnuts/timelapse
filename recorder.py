import json
import os
import time
import picamera
import RPi.GPIO as GPIO

lapse = 0
running = False


def button_pushed():
    global lapse, running
    if not running:
        ++lapse
        running = True
    else:
        running = False


with open(os.path.dirname(os.path.realpath(__file__)) + '/config.json', 'r') as f:
    config = json.load(f)

GPIO.setmode(GPIO.BCM)
GPIO.setup(config['button_pin'], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(config['button_pin'], GPIO.RISING, callback=button_pushed, bouncetime=200)

try:
    while True:
        with picamera.PiCamera() as camera:
            while running:
                for filename in camera.capture_continuous('~/timelapse/img{counter:04d}.jpg'):
                    if config['debug']:
                        print('Captured %s' % filename)
                    time.sleep(config['sleep_seconds'])
                    if not running:
                        break
finally:
    GPIO.cleanup()
