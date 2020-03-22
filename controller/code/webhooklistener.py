from flask_restful import Api, Resource, reqparse
import time
from flask import Flask, request
from OpenSSL import SSL
import json

state = None



class WHListener:
    def index():
    	if request.method == 'GET':
                return '<h1>Hello from Webhook Listener!</h1>'
    	if request.method == 'POST':
                req_data = request.get_json()
                str_obj = json.dumps(req_data)
                print("mottagen: "+str_obj)
                return '{"success":"true"}'

    def __init__(self,startState):
        state = startState
        app = Flask(__name__)
        @app.route('/', methods=['POST','GET'])
        if __name__ == "__main__":
            #context = ('ssl.cert', 'ssl.key')
            # certificate and key file. Cannot be self signed certs
            app.run(host='0.0.0.0', port=5000, threaded=True, debug=True) # will listen on port 5000





"""
class WHListener:
    class Action(Resource):
        def post(self, name):
            print("name = "+ name)
            if name == "open":
                print("open")
                state = "open"

        def get(self, name):
            return name, 200

    def __init__(self,startState):
        state = startState
        self._app = Flask(__name__)
        self._api = Api(self._app)
        self._api.add_resource(Action, "/blinds/")
        print("test1")
        self._app.run(debug=True, host='0.0.0.0')
        print("test2")

whListener = WHListener("closed")
while True:
    print("waiting "+state)
    time.sleep(1000)
"""
