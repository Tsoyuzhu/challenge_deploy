import io
import os
import keras
import string
import helpers

from flask import Flask, Blueprint, render_template
from flask_restplus import Resource, Api, reqparse, fields

from flask import request
from flask import jsonify

os.environ['KERAS_BACKEND']='theano'

app = Flask(__name__, static_url_path='/static')
blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint, doc='/doc/')
app.register_blueprint(blueprint)

print('Loading Keras model...')
helpers.get_model()

a_name = api.model('Name', {'name' : fields.String('The firstname of the person.')})
a_dataset = api.model('Dataset', {'data' : fields.String('A 2D array containing the dataset, entered as a JSON string.')})

@app.route('/')
def index():
    return render_template('index.html')

@api.route('/predict')
class Predict(Resource):
    @api.expect(a_name)
    def post(self):
        prediction = helpers.predict(api.payload['name'])
        result = ['Male','Female']
        return {'result': result[prediction]}

@api.route('/retrain')
class Retrain(Resource):
    @api.expect(a_dataset)
    def post(self):
        # Something strange happens to the model graph if the session is not cleared. The model is reloaded each time as a work around. 
        helpers.get_model() 
        # Flask restful plus does provide good support for defining api models containing lists of lists. Pass data to route as JSON instead.
        data = api.payload
        helpers.retrain_model(data)
        return

if __name__ == '__main__':
    app.run(debug=True)