from flask import Flask, request
# from urllib import unquote_plus
import json
# import re

FILENAME = "blindState"

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
    req_data = req.get_json()
    str_obj = json.dumps(req_data)

    return str_obj

@app.route('/', methods=['GET'])
def index():
    """
    Go to localhost:5000 to see a message
    """
    return ('This is a website.', 200, None)


@app.route('/blinds/close', methods=['POST'])
def closeBlindsRequest():
    file = open(FILENAME, 'w')
    file.write("closed")
    file.close()
    printFile("Skrivet till fil: ")

    return ("Closing", 200, None)



@app.route('/blinds/open', methods=['POST'])
def openBlindsRequest():
    file = open(FILENAME, 'w')
    file.write("open")
    file.close()
    printFile("Skrivet till fil: ")

    return ("Opening", 200, None)

@app.route('/blinds/openslowly', methods=['POST'])
def openBlindsSlowlyRequest():
    file = open(FILENAME, 'w')
    file.write("openslowly")
    file.close()
    printFile("Skrivet till fil: ")

    return ("Opening", 200, None)

def printFile(preString):
    file = open(FILENAME, 'r')
    print(preString + file.read())
    file.close()

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, host='0.0.0.0', port=5000, threaded=True)
    print("test1")
