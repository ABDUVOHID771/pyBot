from flask import Flask, request, jsonify, abort
import requests
import json

app = Flask(__name__)


@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


@app.errorhandler(400)
def resource_not_found(e):
    return jsonify(error=str(e)), 400


@app.route('/hello', methods=['POST'])
def index():
    data = request.json
    if data:
        if 'title' in data and 'message' in data:
            requests.post("https://pyybbot.herokuapp.com/posts",
                          json=data)
            return data
        else:
            abort(400, description="BAD REQUEST")
    else:
        abort(404, description="NOT FOUND")


if __name__ == '__main__':
    app.run(threaded=True)
