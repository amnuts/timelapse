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


try:
    while True:
        with picamera.PiCamera() as camera:
            while running:
                for filename in camera.capture_continuous('img{counter:03d}.jpg'):
                    print('Captured %s' % filename)
                    time.sleep(300)  # wait 5 minutes

    while True:
        if (GPIO.input(10) == False):
            print("Button Pressed")
            os.system('date')  # print the systems date and time
            print GPIO.input(10)
            sleep(5)
        else:
            os.system('clear')  # clear the screens text
            print ("Waiting for you to press a button")
            sleep(0.1)

    with picamera.PiCamera() as camera:
        camera.start_preview()
        try:
            for i, filename in enumerate(camera.capture_continuous('image{counter:02d}.jpg')):
                print(filename)
                time.sleep(1)
                if i == 59:
                    break
        finally:
            camera.stop_preview()

finally:
    GPIO.cleanup()
