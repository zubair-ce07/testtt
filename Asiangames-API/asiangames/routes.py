from flask import jsonify

from asiangames import app


@app.route('/')
def index():
    return jsonify({'message': 'hello'})
