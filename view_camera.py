IMAGE_EFFECTS = [#IMAGE_EFFECTS
  'none',       #0
  'negative',
  'solarize',
  'sketch',     #3
  'denoise',
  'emboss',     #5
  'oilpaint',
  'hatch',
  'gpen',
  'pastel',
  'watercolor',#10
  'film',
  'blur',
  'saturation',
  'colorswap',
  'washedout',#15
  'posterise',
  'colorpoint',
  'colorbalance',
  'cartoon',
  'deinterlace1',
  'deinterlace2',#21
]
import re
from picamera import PiCamera, PiRenderer
from time import sleep

camera = PiCamera( )
camera.resolution = '1200x800'


##camera.hflip = True
camera.rotation = 0


##camera = camera.framerate_range.low
##camera.stero_mode ='side-by-side'
# camera.preview_window(0,0,640,480)

camera.shutter_speed = 33333
camera.framerate = 30
camera.image_effect = IMAGE_EFFECTS[0]

#camera.preview_alpha = 250 

alpha = {'-': -1, '+': 1, '=': 1}
framerateDelta = {'[': -1, ']': 1, '{': -1, '}': 1, }


#These property can be set while recordings or previews are active.
##camera.zoom = (4.0, 0.0, 1.0, 1.0)
##camera.preview_fullscreen = False


# METHODS

def changeEffect(camera, effect):
  try:
    camera.image_effect = effect
    print('image_effect: {0}, params: {1}'.format( camera.image_effect, camera.image_effect_params ))
  except:
    print( 'I dont think thats a effect' )


camera.start_preview()
#camera.start_recording('plasma_loops.h264')
# camera.wait_recording(120)
print(len(IMAGE_EFFECTS))
stroke = "..."
while stroke != "n":
  
  stroke = input('type n to exit\n')
  #Opacity
  if stroke == '+' or stroke == '=' or stroke == '-': 
    preview_alpha = camera.preview_alpha + 10 * alpha[stroke]
    print ( 256 % preview_alpha )
    if preview_alpha < 256 and preview_alpha >= 0:
      camera.preview_alpha = preview_alpha
      print(camera.preview_alpha)
    continue
  
  if stroke == '[' or stroke == ']' or stroke == '{' or stroke == '}':
    camera.framerate_delta = (camera.framerate_delta + 5 * framerateDelta[stroke]) % 60
    print('framerate_delta: {0}'.format(camera.framerate_delta))
    print('framerate: {0}'.format(camera.framerate))

  if stroke == 'set':
    print('image_effect_params {0}'.format(camera.image_effect_params))
    
#only numbers from here
  pattern = re.compile("[0-9]")
  if not pattern.match(stroke) and stroke != 'n':
    print("not a number")
    continue
  # image effects
  if stroke != 'n' and int(stroke) < len(IMAGE_EFFECTS) :
    changeEffect(camera, IMAGE_EFFECTS[int(stroke)])
    # camera.image_effect = IMAGE_EFFECTS[int(stroke)]
    # print( IMAGE_EFFECTS[int(stroke)] )




print("closing")
sleep(1)
#camera.stop_recording()

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
