# -*- coding: utf-8 -*-

import json
from flask import Flask, jsonify, abort
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def hello():
    return 'hello:)'


@app.route('/api/', methods=['GET'])
def get():
    return jsonify(read_model())


@app.route('/api/<school_id>/', methods=['GET'])
def get_school_info(school_id):
    # TODO: KeyError の Handling
    school_info = get_model()[school_id]
    return jsonify(school_info)


@app.route('/404')
def abort404():
    abort(404)


def get_model():
    """ Get model """
    return read_model()


def read_model():
    """ Load JSON """
    file_name = "data/data.json"
    try:
        with open(file_name, 'r') as f:
            return json.load(f)
    except IOError as e:
        print(e)
        return None


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
