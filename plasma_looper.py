from time import sleep
from picamera import PiCamera
import re,os,glob
IMAGE_EFFECTS = [  # IMAGE_EFFECTS
    'none',  # 0
    'negative',
    'solarize',
    'sketch',  # 3
    'denoise',
    'emboss',  # 5
    'oilpaint',
    'hatch',
    'gpen',
    'pastel',
    'watercolor',  # 10
    'film',
    'blur',
    'saturation',
    'colorswap',
    'washedout',  # 15wifi2600
    'posterise',
    'colorpoint',
    'colorbalance',
    'cartoon',
    'deinterlace1',
    'deinterlace2',  # 21
]
window=(300,100,1296, 972)
#import glob
#import os

camera = PiCamera(  )
#camera.resolution = '800x750'
def getOptions():
  print('resolution is: '+ str(camera.resolution)+'\n')
  txt=input('filename? enter for default')
  #parse resolution demensions from input 
  # set new camera resolution
  options=txt.split(',')
  optionsObj = {}
  for i in options:
    KV=i.split('=')
    if len(KV) == 2:
      k,v=KV
      optionsObj[k]=v
  return optionsObj

#options = getOptions()
#print(options)
#filename = input('filename? or press enter \n')
print('start looping space cowboy')

#camera.hflip = True
camera.rotation = 0


#camera = camera.framerate_range.low
##camera.stero_mode ='side-by-side'
# camera.preview_window(06,0,640,480)

camera.shutter_speed = 33333
print(camera.framerate) # = 35 
camera.image_effect = IMAGE_EFFECTS[0]

#camera.preview_alpha = 250

alpha = {'-': -1, '+': 1, '=': 1}
framerateDelta = {'[': -1, ']': 1, '{': -1, '}': 1, }


# These property can be set while recordings or previews are active.
##camera.zoom = (4.0, 0.0, 1.0, 1.0)
##camera.preview_fullscreen = False


# METHODS

def changeEffect(camera, effect):
    try:
        camera.image_effect = effect
        print('image_effect: {0}, params: {1}'.format(
            camera.image_effect, camera.image_effect_params))
    except:
        print('I dont think thats a effect')
def xy():
  txt = input("press return") or " ."
  print(txt + '++')
  txt=txt.split()
  #print(txt)
  x=txt[0]
  if x.isnumeric():
    y='txt[1]'
    if x:

      print('yes')
#def convertObjToInput(obj):
#  for i in obj:
hasWindow = 'window' not in globals()

camera.start_preview(fullscreen= hasWindow, window=window)

print(len(IMAGE_EFFECTS))
stroke = "..."
while stroke != "n":

  stroke = input('type n to exit\n')
  if stroke == ' ':
    imgs=glob.glob('*.'+ 'jpg')
    imgCount = len(imgs)
    imagename = 'snap_'+str(imgCount)+'.jpg'
    # scp pi@raspberrypi:/tmp/picture.jpg ~/site/pi/
    print('snap')
    camera.wait_recording(1)
    camera.capture(imagename, use_video_port=True)
    camera.wait_recording(1)
    print(imagename)
  # Opacity
  if stroke == '+' or stroke == '=' or stroke == '-':
    preview_alpha = camera.preview_alpha + 10 * alpha[stroke]
    print(256 % preview_alpha)
    if preview_alpha < 256 and preview_alpha >= 0:
        camera.preview_alpha = preview_alpha
        print(camera.preview_alpha)
    continue
  # frame rate/ speed
  if stroke == '{' or stroke == '}':
    camera.framerate = (camera.framerate + 3 * framerateDelta[stroke]) % 60
    print('framerate: {0}'.format(camera.framerate))
  if stroke == '[' or stroke == ']':
    camera.framerate_delta = (
        camera.framerate_delta + 3 * framerateDelta[stroke]) % 60
    print('framerate_delta: {0}'.format(camera.framerate_delta))
  #  if stroke == 'rec' or stroke =='R':
  #    videoFolderName="recordings"
  #    continue
  #    videos= glob.glob("*.h264")
  #    print(videos, num, cwd)
  #    continue
  #    num=len(videos)
  #    cwd=os.getcwd()

  #    continue
  #    folderExists = os.path.exists(cwd + "/"+ videoFolderName)
  #    if folderExists == False:
  #       print('making ./'+videoFolderName+'for the video')
  #       os=mkdir( videoFolderName )
    #camera.start_recording('./'+videoFolder+ 'test''.h264')
  #   print('plasma_loops'+str(num)+'.h264')
    # camera.wait_recording(120)
  #    continue
  if stroke == 'eval':
    code=input('input code\n')
    try:
      eval(code)
    except:
      print('nah')
    continue
  if stroke == 'rec' or stroke == 'R':
    format='h264'

    videos=glob.glob('*.'+format)
    print('filming') 
    count = len(videos)
    hasFileName = len(filename) != 0

    if hasFileName:
      filename = filename + '.' + format
    else:
      filename = 'loop'+str(count)+'.' + format
    print(filename, count)
    sleep(1)
    camera.start_recording(filename)
    #camera.start_recording('loop_'+str(len(videos))+'.h264')
    sleep(1)
    continue
  if stroke == 'stop' or stroke == 'S':
    camera.stop_recording()
    continue
  if stroke == 'set':
    print('image_effect_params {0}'.format(camera.image_effect_params))
    continue

  
  # only numbers from here
  pattern = re.compile("[0-9]")
  if not pattern.match(str(stroke)) and stroke != 'n':
    print("not a number")
    continue
  # image effects
  if stroke != 'n' and int(stroke) < len(IMAGE_EFFECTS):
    changeEffect(camera, IMAGE_EFFECTS[int(stroke)])
    # camera.image_effect = IMAGE_EFFECTS[int(stroke)]
    # print( IMAGE_EFFECTS[int(stroke)] )


print("closing")
if camera._check_recording_stopped():
    sleep(1)
    camera.stop_recording()
    print('stopping any recordings')
sleep(1)
# for x in range(0, len(IMAGE_EFFECTS)):
# #   # camera.framerate_delta = camera.framerate + x * 10
# #   # print(camera.framerate + camera.framerate_delta)
# #   camera.image_effect = IMAGE_EFFECTS[x]
# #   print(IMAGE_EFFECTS[x])
# #   print( camera.image_effect_params )
# #   camera.led = not camera.led
#   sleep(6)

camera.stop_preview()


# Can i output video in formats otherthan .h264?

# No. Raspivid only supports raw h.264.
# You either

# 1) need to mux the file after recording with MP4Box or
# 2) rewrite raspivid to mux on-the-fly (with ffmpeg ??) or
# 3) use a gstreamer pipeline which records directly to a "proper" format

