from flask import Flask
from flask_restful import Api, Resource, reqparse
import time

state = None

class Action(Resource):
    def post(self, name):
        print("name = "+ name)
        if name == "open":
            print("open")
            state = "open"

    def get(self, name):
        return name, 200

class WHListener:
    def __init__(self,startState):
        state = startState
        self._app = Flask(__name__)
        self._api = Api(self._app)
        self._action = Action()
        self._api.add_resource(self._action, "/blinds/")
        print("test1")
        self._app.run(debug=True, host='0.0.0.0')
        print("test2")

whListener = WHListener("closed")
while True:
    print("waiting "+state)
    time.sleep(1000)
