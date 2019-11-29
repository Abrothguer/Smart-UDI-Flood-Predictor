from flask import Flask, jsonify
from flask_cors import CORS

APP = Flask(__name__)
CORS(APP)

data = [
    {
        "name": "Rondon",
        "lat": -18.932131,
        "lon": -48.282762,
        "wind": 1.2,
        "temp": 30,
        "status": "Alagada",
        "danger": "Alto"
    },
    {
        "name": "Terminal",
        "lat": -18.9128,
        "lon": -48.2755,
        "wind": 1.2,
        "temp": 30,
        "status": "Alagada",
        "danger": "Baixo"
    },
    {
        "name": "Joao Naves",
        "lat": -18.919505,
        "lon": -48.261878,
        "wind": 1.2,
        "temp": 30,
        "status": "Alagada",
        "danger": "Medio"
    }
]

@APP.route('/hw')
def helloworld():
    return 'Hello World'

@APP.route('/getData')
def get_data():
    return jsonify(data)

def main():
    APP.run(host='0.0.0.0', debug=True, port=7059)


if __name__ == "__main__":
    main()
