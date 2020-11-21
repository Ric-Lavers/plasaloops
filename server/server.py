#! python3
import sys, requests
from flask import Flask,jsonify,request,render_template
import re,os,glob
from picamera import PiCamera
#import logging
from constants import IMAGE_EFFECTS,get_ip
IMAGE_EFFECTS=IMAGE_EFFECTS.IMAGE_EFFECTS
get_ip=get_ip.get_ip

PORT=5000
#logger = logging.getLogger()
camera = PiCamera()
camera.resolution = '800x800'

global window,filename
window=(0,0,0,0)
filename='loop'

app = Flask(__name__)
#print(dir(camera))
#print ( str(sys.argv))

#store current ip remotely
ip=get_ip() + ':' + str(PORT)
try:
  requests.post('https://skribbl-lists-serverless.now.sh/api/ip/replace', data={"ip": ip})
except Exception as e:
  print(jsonify(e)) 

# get inital state
@app.route('/init')
def get_inital():
  return jsonify({
    'previewing': camera.previewing,
    'recording': camera.recording,
    'image_effect': camera.image_effect,
    'resolution': camera.resolution,
    'preview_window': camera.preview_window if camera.preview_window != None else window,
  })

# start camera
@app.route('/start')
def start_cam():
  print('start camera')
  fs = True if window[3] == 0 or window[2] == 0 else False
  camera.start_preview(fullscreen=fs, window=window)
  return 'start camera'

#stop camera
@app.route('/stop')
def stop_cam():
  print('stop camera')
  camera.stop_preview()
  return 'stop camera'

def get_filename():
  filename = globals()['filename']
  Format='h264'
  list_of_videos=glob.glob(filename+'*.'+Format)
  count = len(list_of_videos)

  if count == 0:
    filename = filename + '.' + Format
  else:
    filename = filename+'_'+str(count)+'.' + Format
  return filename

#record file
@app.route('/start_recording', methods=['POST','GET'])
def start_recording():

  d=request.get_json()
  if 'filename' in d:
    globals()['filename'] = d['filename']
  fn = get_filename()
  print(fn)
  camera.start_recording(fn)
  return jsonify({'success': True, 'message': 'started recording as "'+fn +'"'})

@app.route('/stop_recording')
def stop_recording():
  camera.stop_recording()
  return jsonify({'success': True, 'message': 'ended recording as "'+get_filename() +'"'})

#setters
@app.route('/set_res', methods=['POST'])
def set_res():
  d=request.get_json()
  print(d)
  camera.resolution= (int(d['width']),int(d['height']))
  return jsonify({'success': True})

@app.route('/set_window', methods=['POST'])
def set_window():
  try:
    d=request.get_json()
    globals()['window']=(int(d['x']),int(d['y']),int(d['height']),int(d['width']))
    if camera.previewing:
      start_cam()
    return jsonify({'success': True})
  except Exception as e:
    return jsonify(e)

#get /effect
@app.route('/effect')
def get_effects():
  print(request)
  return jsonify({'current': camera.image_effect ,'IMAGE_EFFECTS': IMAGE_EFFECTS})
    

#post /effect data: {effect:}
@app.route('/effect' , methods=['POST'])
def change_effect():
  try:
    request_data = request.get_json()
    newEffect = request_data["effect"]
    if newEffect not in IMAGE_EFFECTS:
      raise
    camera.image_effect = newEffect
    return jsonify({ 'effect': newEffect })
  except Exception as e:
    print(str(e))
    return 'I dont think thats a effect'

@app.before_request
def filter_prefetch():
# uncomment these to filter Chrome specific prefetch requests.
  if 'Purpose' in request.headers and request.headers.get('Purpose') == 'prefetch':
    return ''


@app.after_request
def debug_after(response):
  header=response.headers
  header['Access-Control-Allow-Origin'] = '*'
  header['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
  header['Access-Control-Allow-Methods'] = 'OPTIONS, HEAD, GET, POST, DELETE, PUT'

  response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
  response.headers["Pragma"] = "no-cache"
  response.headers["Expires"] = "0"
  response.headers['Cache-Control'] = 'public, max-age=0'
  response.headers['Connection'] = 'close'
  return response


ip=get_ip()

app.run(
  host=ip, 
  port=PORT,
  threaded=True
)
