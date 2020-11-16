import re
from picamera import PiCamera

import time


camera = PiCamera( )
camera.resolution = '800x800'
sleep = 800

camera.start_preview()
time.sleep(sleep)
camera.stop_preview()
