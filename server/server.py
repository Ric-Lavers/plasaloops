from flask import Flask,jsonify,request,render_template
from picamera import PiCamera
from constants import IMAGE_EFFECTS
IMAGE_EFFECTS=IMAGE_EFFECTS.IMAGE_EFFECTS

camera = PiCamera()
camera.resolution = '800x800'

app = Flask(__name__)

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
    return 'changed to {}'.format(newEffect)
  except:
    return 'I dont think thats a effect'



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
  host='localhost', 
  port=5000
)