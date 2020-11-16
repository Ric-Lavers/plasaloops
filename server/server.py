from flask import Flask,jsonify,request,render_template
from picamera import PiCamera
#import logging
from constants import IMAGE_EFFECTS
IMAGE_EFFECTS=IMAGE_EFFECTS.IMAGE_EFFECTS

#logger = logging.getLogger()
camera = PiCamera()
camera.resolution = '800x800'

app = Flask(__name__)

# get inital state
@app.route('/init')
def initalise():
  return jsonify({
    previewing: camera.previewing,
    recording: camera.recording,
    image_effect: camera.image_effect,
    resolution: camera.resolution,
  })

# start camera
@app.route('/start')
def start_cam():
  print('start camera')
  camera.start_preview()
  return 'start camera'

#stop camera
@app.route('/stop')
def stop_cam():
  print('stop camera')
  camera.stop_preview()
  return 'stop camera'

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
    logger.debug("prefetch requests are not allowed")
    return '', status.HTTP_403_FORBIDDEN


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



#demo

stores = [{
    'name': 'My Store',
    'items': [{'name':'my item', 'price': 15.99 }]
}]

@app.route('/')
def home():
  return  "hello world"
  return render_template('index.html')

#post /store data: {name :}
@app.route('/store' , methods=['POST'])
def create_store():
  request_data = request.get_json()
  new_store = {
    'name':request_data['name'],
    'items':[]
  }
  stores.append(new_store)
  return jsonify(new_store)
  #pass

#get /store/<name> data: {name :}
@app.route('/store/<string:name>')
def get_store(name):
  for store in stores:
    if store['name'] == name:
          return jsonify(store)
  return jsonify ({'message': 'store not found'})
  #pass

#get /store
@app.route('/store')
def get_stores():
  return jsonify({'stores': stores})
  #pass

#post /store/<name> data: {name :}
@app.route('/store/<string:name>/item' , methods=['POST'])
def create_item_in_store(name):
  request_data = request.get_json()
  for store in stores:
    if store['name'] == name:
        new_item = {
            'name': request_data['name'],
            'price': request_data['price']
        }
        store['items'].append(new_item)
        return jsonify(new_item)
  return jsonify ({'message' :'store not found'})
  #pass

#get /store/<name>/item data: {name :}
@app.route('/store/<string:name>/item')
def get_item_in_store(name):
  for store in stores:
    if store['name'] == name:
        return jsonify( {'items':store['items'] } )
  return jsonify ({'message':'store not found'})

  #pass

app.run(
  host='192.168.1.123', 
  port=5000,
  threaded=True
)
