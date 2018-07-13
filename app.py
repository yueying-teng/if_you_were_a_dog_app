from __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob
import re
import numpy as np
import pickle  

# Keras
from keras.models import load_model
from keras.preprocessing import image

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

# Define a flask app
app = Flask(__name__)



# load pickled name_dict
infile = open('models/name_dict','rb')
name_dict = pickle.load(infile)
infile.close()



# Model saved with Keras model.save()
MODEL_PATH = 'models/model_deploy.h5'

# Load your trained model
model = load_model(MODEL_PATH)
model._make_predict_function()          # Necessary
print('Model loaded. Start serving...')

# You can also use pretrained model from Keras
# Check https://keras.io/applications/
# from keras.applications.resnet50 import ResNet50
# model = ResNet50(weights='imagenet')
# print('Model loaded. Check http://127.0.0.1:5000/')


INPUT_SIZE = 299

def model_predict(img_path, model):
    """
    to make prediction
    """
    img = image.load_img(img_path, target_size = (INPUT_SIZE, INPUT_SIZE))

    # Preprocessing the image
    x = image.img_to_array(img)
    x = np.true_divide(x, 255)
    x = np.expand_dims(x, axis=0)

    preds = model.predict(x)
    return preds


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = model_predict(file_path, model)

    
        # predicted label
        pred_label = np.argsort(- preds)[0][0]
        # pred_prob = np.sort(- preds)[0] * -1.  # prediction probabilities 
        pred_class = []
        # return breed name from predicted label, the most confident prediction only
        pred_class.append(list(name_dict.keys())[list(name_dict.values()).index(pred_label)])
        
        # Convert to string
        result = str(pred_class[0])              
        
        return result
    return None


if __name__ == '__main__':
    # app.run(port=5002, debug=True)
    app.run()

    # Serve the app with gevent
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
