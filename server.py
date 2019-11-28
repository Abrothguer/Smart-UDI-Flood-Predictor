from flask import Flask
from flask_cors import CORS

APP = Flask(__name__)
CORS(APP)

@APP.route('/hw')
def helloworld():
    return 'Hello Andre'


def main():
    APP.run(host='0.0.0.0', debug=True, port=7059)


if __name__ == "__main__":
    main()
