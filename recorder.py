import json
import os
import threading
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


def flash_led(times, long_end=False):
    global config
    for x in range(times):
        if config['debug']:
            print('Flash LED %d' % filename)
        GPIO.output(config['led_pin'], 1)
        time.sleep(0.5)
        GPIO.output(config['led_pin'], 0)
    if long_end:
        GPIO.output(config['led_pin'], 1)
        time.sleep(2)
        GPIO.output(config['led_pin'], 0)


with open(os.path.dirname(os.path.realpath(__file__)) + '/config.json', 'r') as f:
    config = json.load(f)

GPIO.setmode(GPIO.BCM)
GPIO.setup(config['led_pin'], GPIO.OUT)
GPIO.setup(config['button_pin'], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(config['button_pin'], GPIO.RISING, callback=button_pushed, bouncetime=200)

try:
    t = threading.Thread(target=flash_led, args=[3, True])
    t.start()
    while True:
        with picamera.PiCamera() as camera:
            while running:
                for filename in camera.capture_continuous(config['save_path'] % lapse):
                    if config['debug']:
                        print('Captured %s' % filename)
                    time.sleep(config['sleep_seconds'])
                    t = threading.Thread(target=flash_led, args=[1])
                    t.start()
                    if not running:
                        break
finally:
    GPIO.cleanup()
