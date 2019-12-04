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

CLIMATE_KEY = ''
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
        },
        {
            "name": "Avenida Rondon Pacheco",
            "lat": -18.914708,
            "lon": -48.262847,
            "status": "Alagada",
            "danger": "Alto",
            "area": 'Altíssimo',
            "pluv": 30,
            "alt": 837,
            "imperm": "Alta"
        },
        {
            "name": "Avenida Rondon Pacheco",
            "lat": -18.917873,
            "lon": -48.265971,
            "status": "Alagada",
            "danger": "Alto",
            "area": 'Altíssimo',
            "pluv": 30,
            "alt": 836,
            "imperm": "Alta"
        },
        {
            "name": "Avenida Rondon Pacheco",
            "lat": -18.904526,
            "lon": -48.260331,
            "status": "Alagada",
            "danger": "Alto",
            "area": 'Altíssimo',
            "pluv": 30,
            "alt": 836,
            "imperm": "Alta"
        },
        {
            "name": "Avenida João Naves de Ávila c/ Rua Prata",
            "lat": -18.910272,
            "lon": -48.264727,
            "status": "Alagada",
            "danger": "Alto",
            "area": 'Altíssimo',
            "pluv": 30,
            "alt": 836,
            "imperm": "Alta"
        },
        {
            "name": "Avenida Cesário Alvim c/ Rua Niterói",
            "lat": -18.905733,
            "lon": -48.264730,
            "status": "Alagada",
            "danger": "Medio",
            "area": 'Altíssimo',
            "pluv": 30,
            "alt": 836,
            "imperm": "Alta"
        },
        {
            "name": "Avenida Montreal",
            "lat": -18.901137,
            "lon": -48.251823,
            "status": "Alagada",
            "danger": "Alto",
            "area": 'Altíssimo',
            "pluv": 30,
            "alt": 836,
            "imperm": "Alta"
        },
        {
            "name": "Rua Coronel Tobias Junqueira",
            "lat": -18.928005,
            "lon": -48.296280,
            "status": "Alagada",
            "danger": "Alto",
            "area": 'Altíssimo',
            "pluv": 30,
            "alt": 836,
            "imperm": "Alta"
        },
        {
            "name": "Avenida Getúlio Vargas",
            "lat": -18.922185,
            "lon": -48.288623,
            "status": "Alagada",
            "danger": "Alto",
            "area": 'Altíssimo',
            "pluv": 30,
            "alt": 836,
            "imperm": "Alta"
        },
        {
            "name": "Avenida Geraldo Abrão c/ Rua Saldanha Marinho",
            "lat": -18.940029,
            "lon": -48.242280,
            "status": "Alagada",
            "danger": "Medio",
            "area": 'Altíssimo',
            "pluv": 30,
            "alt": 836,
            "imperm": "Alta"
        },
        {
            "name": "Alameda Uberaba",
            "lat": -18.925048,
            "lon": -48.259292,
            "status": "Alagada",
            "danger": "Medio",
            "area": 'Altíssimo',
            "pluv": 30,
            "alt": 836,
            "imperm": "Alta"
        },
              {
            "name": "Avenida Antônio Thomaz Ferreira Rezende",
            "lat": -18.880718,
            "lon": -48.271493,
            "status": "Alagada",
            "danger": "Medio",
            "area": 'Altíssimo',
            "pluv": 30,
            "alt": 836,
            "imperm": "Alta"
        },
        {
            "name": "Rua Olegário Maciel",
            "lat": -18.927684,
            "lon": -48.268149,
            "status": "Alagada",
            "danger": "Medio",
            "area": 'Altíssimo',
            "pluv": 30,
            "alt": 836,
            "imperm": "Alta"
        },
        {
            "name": "Avenida Marcos de Freitas Costas",
            "lat": -18.912274,
            "lon": -48.302384,
            "status": "Alagada",
            "danger": "Alto",
            "area": 'Altíssimo',
            "pluv": 30,
            "alt": 836,
            "imperm": "Alta"
        },
        {
            "name": "Avenida Raulino Cotta Pacheco",
            "lat": -18.912773,
            "lon": -48.286725,
            "status": "Alagada",
            "danger": "Medio",
            "area": 'Altíssimo',
            "pluv": 30,
            "alt": 836,
            "imperm": "Alta"
        },
        {
            "name": "Avenida Silvio Rugani",
            "lat": -18.929961,
            "lon": -48.293760,
            "status": "Alagada",
            "danger": "Alto",
            "area": 'Altíssimo',
            "pluv": 30,
            "alt": 836,
            "imperm": "Alta"
        },
        {
            "name": "Praça Rita Huguiney Ferreira",
            "lat": -18.929050,
            "lon": -48.300926,
            "status": "Alagada",
            "danger": "Medio",
            "area": 'Altíssimo',
            "pluv": 30,
            "alt": 836,
            "imperm": "Alta"
        },
        {
            "name": "Felipe Calixto Milken",
            "lat": -18.915099,
            "lon": -48.188927,
            "status": "Alagada",
            "danger": "Alto",
            "area": 'Altíssimo',
            "pluv": 30,
            "alt": 836,
            "imperm": "Alta"
        },
        {
            "name": "Avenida Judeia",
            "lat": -18.954440,
            "lon": -48.329131,
            "status": "Alagada",
            "danger": "Alto",
            "area": 'Altíssimo',
            "pluv": 30,
            "alt": 836,
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
    try:
        get_sensor_data()
    except:
        pass
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


MSG_SENT = False
def send_message(msg):
    
    global MSG_SENT
    if MSG_SENT:
        return
    
    MSG_SENT = True
    print('Actually sending it ....')
    # Your Account Sid and Auth Token from twilio.com/console
    # DANGER! This is insecure. See http://twil.io/secure
    account_sid = ''
    auth_token = ''
    client = Client(account_sid, auth_token)

    numbers = ['+55034991301011', '+5534998826478', '+5534999770352']

    for number in numbers:
        client.messages \
                        .create(
                            body=msg,
                            from_='+12015146109',
                            to=number
                        )

THRESHOLD = 40
def get_sensor_data():

    sensordata = requests.get('http://' + IP_SENSOR).content
    print('DATA IS', sensordata)

    pluv = json.loads(sensordata)["US_0"]
    if pluv < 0:
        pluv = 0

    if pluv > THRESHOLD:
        print("Sending message...")
        send_message("AVISO: Alagamento na Av. Rondon Pacheco.")

    data["markers"][0]["pluv"] = pluv
    data["markers"][1]["pluv"] = pluv
    data["markers"][2]["pluv"] = pluv
    # data["markers"] = map(mapfunc, data["markers"])


def main():
    get_climate_data()
    APP.run(host='0.0.0.0', debug=True, port=7059)


if __name__ == "__main__":
    main()
