
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import numpy as np
import face_recognition
import pickle
import base64
from io import BytesIO
from PIL import Image
import tensorflow as tf
from tensorflow.keras.models import load_model


Image_size=224


def predict(model, img):
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)

    predictions = model.predict(img_array)
    confidence = round(100 * (np.max(predictions[0])), 2)

    if(predictions[0]>0.95 and confidence>95.00):
        predicted_class='Real'
    else:
        predicted_class='Fake'
    return predicted_class, confidence




app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Load known face encodings
with open("EncodeFile.p", 'rb') as file:
    encodelistknownwithnameandid = pickle.load(file)
    knownencodelist, Names, Ids = encodelistknownwithnameandid
  


def preprocess_image(image_data):
    image = Image.open(BytesIO(image_data))
    image = image.resize((0.25 * np.array(image.size)).astype(int))  
    np_image = np.array(image)
    return np_image

@app.route('/recognize', methods=['POST'])
@cross_origin()
def recognize_face():
    model=load_model(r"D:\my projects\MOBILE APPLICATIONS\HR\HR\Backend\Antispoofing\Model\1.h5")
    if 'image' and 'Id' not in request.json:
        return jsonify({'error': 'Image data not provided', 'state': False})

    # Decode and process the image
    Id= request.json['Id']
    image_data = request.json['image']
    image_data = base64.b64decode(image_data.split(',')[1])
    np_image = preprocess_image(image_data)

    predictedClass=predict(model,np_image)
    print(predictedClass[0])
    if(predictedClass[0]=='Real'):
        face = face_recognition.face_locations(np_image)
        encodecur_image = face_recognition.face_encodings(np_image, face)

        if not encodecur_image:
          return jsonify({'error': 'No face found in the image', 'state': False})

        encodecur_image = encodecur_image[0]  # Use the first encoding found

    # Compare faces
        matches = face_recognition.compare_faces(knownencodelist, encodecur_image)
        faceDis = face_recognition.face_distance(knownencodelist, encodecur_image)

        if len(faceDis) == 0:
          return jsonify({'error': 'No faces recognized', 'state': False})

        index = np.argmin(faceDis)
        print(type(Id))
        print(str(Ids[index]))
        print(matches[index])
   

        if matches[index] and str(Ids[index])==Id:
          return jsonify({'datas':{'Id':str(Ids[index]),'name':Names[index]} , 'state': True})
    
        else:
          return jsonify({'error': 'Face not recognaized', 'state': False})

    else:
       return jsonify({'error':'You are not Live','state':False})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)