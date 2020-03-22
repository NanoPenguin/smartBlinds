from flask import Flask, request
# from urllib import unquote_plus
import json
# import re

app = Flask(__name__)

def parse_request(req):
    """
    Parses application/json request body data into a Python dictionary
    """
    """
    payload = req.get_data()
    payload = unquote_plus(payload)
    payload = re.sub('payload=', '', payload)
    payload = json.loads(payload)
    """

    return json.loads(req.get_data().decode('utf-8'))

@app.route('/', methods=['GET'])
def index():
    """
    Go to localhost:5000 to see a message
    """
    return ('This is a website.', 200, None)


@app.route('/blinds/close', methods=['POST'])
def closeBlindsRequest():
    payload = parse_request(request)
    print("Mottaget: "+payload)
    return ("Closing", 200, None)


@app.route('/blinds/open', methods=['POST'])
def openBlindsRequest():
    payload = parse_request(request)
    print("Mottaget: "+payload)
    return ("Opening", 200, None)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, host='0.0.0.0', port=5000, threaded=True)
    print("test1")
