import json
import os
import threading
import time
import picamera
import RPi.GPIO as GPIO

lapse = 0
running = False


def button_pushed(channel):
    global lapse, running
    if config['debug']:
        print('Button on pin %d pushed' % channel)
        ++lapse
        if not running:
            print('Starting capture run %d' % lapse)
        running = True
    else:
        if not running:
            print('Ending capture run %d' % lapse)
        running = False


def flash_led(times, long_end=False):
    global config
    if config['debug']:
        print('Running LED thread')
    for x in range(times):
        if config['debug']:
            print('Flash number %d' % x)
        GPIO.output(config['led_pin'], 1)
        time.sleep(0.5)
        GPIO.output(config['led_pin'], 0)
        time.sleep(0.5)
    if long_end:
        if config['debug']:
            print('Long end light')
        GPIO.output(config['led_pin'], 1)
        time.sleep(2)
        GPIO.output(config['led_pin'], 0)

print('Loading timelapse capture software')

with open(os.path.dirname(os.path.realpath(__file__)) + '/config.json', 'r') as f:
    config = json.load(f)

if config['debug']:
    print('Setting pins and callback')

GPIO.setmode(GPIO.BCM)
GPIO.setup(config['led_pin'], GPIO.OUT)
GPIO.setup(config['button_pin'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(config['button_pin'], GPIO.RISING, callback=button_pushed, bouncetime=200)

if config['debug']:
    print('Entering main loop')

try:
    if config['debug']:
        print('Kicking off start-up LED flash')
    t = threading.Thread(target=flash_led, args=[3, True])
    t.start()
    while True:
        with picamera.PiCamera() as camera:
            while running:
                if config['debug']:
                    print('In run loop')
                for filename in camera.capture_continuous(config['save_path'] % lapse):
                    if config['debug']:
                        print('Captured %s and starting LED flash' % filename)
                    t = threading.Thread(target=flash_led, args=[1])
                    t.start()
                    if config['debug']:
                        print('Sleeping')
                    time.sleep(config['sleep_seconds'])
                    if not running:
                        if config['debug']:
                            print('No longer running so break out of loop')
                        break
            if config['debug']:
                print('Not capturing on this loop')
finally:
    GPIO.cleanup()
