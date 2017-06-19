time lapse
===

A small time lapse script that will start recording when you press the button and stop recording when you press the button again.

Each group of recordings are in their own directory.

It's not terribly configurable as it was just put together for my son's homework, but also an opportunity for me just to play with threads and such in Python.

autostart
---
To autostart the script on boot you can simply add a cron entry.  To do this, I would modify the crontab for _pi_ user with:

    $ sudo crontab -u pi -e

and then add the line:

    @reboot python /home/pi/timelapse/recorder.py &

led
---

When the script starts up the led will flash a few times and then go solid for a little bit.  After pressing the button to run start the time lapse the led will flash when a photo is taken.

debug
---

There is lots of debug output which can be turned off via the configuration file.
