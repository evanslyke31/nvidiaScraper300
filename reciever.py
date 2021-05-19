import flask
from flask import request
import os
app = flask.Flask(__name__)


@app.route('/', methods=['POST'])
def post_url():
    print(request)
    os.popen("chrome %s" % request.data.decode())
    return "success"

if __name__ == '__main__':
    app.run(host="localhost", port=10025, debug=True)