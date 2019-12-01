import threading
import requests
import json

from flask import Flask, jsonify
from flask_cors import CORS

from twilio.rest import Client

import cv2
import numpy as np
import tensorflow as tf

from keras.models import load_model, model_from_json
from keras import backend as K

APP = Flask(__name__)
CORS(APP)

CLIMATE_KEY = 'c89ebea0'
IMG_SIZE = 75
NB_CHANNELS = 3
BATCH_SIZE = 32
NB_TRAIN_IMG = 1800
NB_VALID_IMG = 600

IP_SENSOR = '169.254.119.141'


data = {
    "markers": [
        {
            "name": "Avenida Rondon Pacheco",
            "lat": -18.932131,
            "lon": -48.282762,
            "status": "Alagada",
            "danger": "Alto",
            "area": 'Altíssimo',
            "pluv": 30,
            "alt": 790,
            "imperm": "Alta"
        },
        {
            "name": "Avenida João Pinheiro",
            "lat": -18.9128,
            "lon": -48.2755,
            "status": "Alagada",
            "danger": "Baixo",
            "area": 'Médio',
            "pluv": 28,
            "alt": 872,
            "imperm": "Alta"
        },
        {
            "name": "Avenida João Naves de Ávila",
            "lat": -18.919505,
            "lon": -48.261878,
            "status": "Alagada",
            "danger": "Medio",
            "area": 'Baixo',
            "pluv": 30,
            "alt": 860,
            "imperm": "Alta"
        }
    ],
    "climate": {

    }
}

try:
    with open('cnn.json','r') as f:
        model_json = json.load(f)
    model = model_from_json(model_json)
    model.load_weights('cnn.h5')

    model.compile(loss = 'binary_crossentropy', optimizer = 'rmsprop', metrics = ['accuracy'])

    img = cv2.imread('data/test/Enchente/f27.jpg')
    # img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    # np.resize(img, (-1, IMG_SIZE, IMG_SIZE, 3))
    img = np.expand_dims(img, axis=0)

    classes = model.predict(img)
    print(classes)
except:
    pass


@APP.route('/hw')
def helloworld():
    return 'Hello World'


@APP.route('/getData')
def get_data():
    get_sensor_data()
    return jsonify(data)


def get_climate_data():

    try:
        response = requests.get("https://api.hgbrasil.com/weather?woeid=455917&key=" + CLIMATE_KEY).json()
        threading.Timer(5.0, get_climate_data).start()
        results = response["results"]
        data["climate"] = {
            "time": results["time"],
            "temp": results["temp"],
            "description": results["description"],
            "humidity": results["humidity"],
            "wind": results["wind_speedy"]
        }
    except:
        pass


def send_message(msg):
    
    # Your Account Sid and Auth Token from twilio.com/console
    # DANGER! This is insecure. See http://twil.io/secure
    account_sid = 'AC3600578906547cadb70af55cb850eebe'
    auth_token = '3407c1e7bca46941371f70d6788c0f49'
    client = Client(account_sid, auth_token)

    numbers = ['+55034991301011']

    for number in numbers:
        client.messages \
                        .create(
                            body=msg,
                            from_='+12015146109',
                            to=number
                        )


def get_sensor_data():

    sensordata = requests.get('http://' + IP_SENSOR).content
    print('DATA IS', sensordata)

    pluv = json.loads(sensordata)["US_0"]
    if pluv >= 30:
        pluv = 0

    data["markers"][0]["pluv"] = pluv
    data["markers"][1]["pluv"] = pluv
    data["markers"][2]["pluv"] = pluv
    # data["markers"] = map(mapfunc, data["markers"])


def main():
    get_climate_data()
    APP.run(host='0.0.0.0', debug=True, port=7059)


if __name__ == "__main__":
    main()
