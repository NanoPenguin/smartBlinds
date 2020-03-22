from flask import Flask
from flask_restful import Api, Resource, reqparse

state = None

class Action(Resource):
    def post(self, name):
        if name == "open":
            print("open")
            state = "open"

    def get(self, name):
        return name, 200

class WHListener:
    def WHListener(self,startState):
        state = startState
        self._app = Flask(__name__)
        self._api = Api(app)
        self._api.add_resource(Action, "/blinds/")
        self._app.run(debug=True, host='0.0.0.0')
