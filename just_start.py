import re
from picamera import PiCamera, PiRenderer
from time import sleep

camera = PiCamera( )
camera.resolution = '1600x800'
sleep = 300

camera.start_preview()
sleep(sleep)
camera.stop_preview()
