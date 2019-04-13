from flask import Flask, request
from flask_restful import Resource, Api
import garden_logic

app = Flask(__name__)
api = Api(app)


class Pots(Resource):
    def __init__(self):
        self.logic_wrapper = garden_logic.Pots()

    def get(self):
        return self.logic_wrapper.json_wrap.data

    def post(self):
        json = request.get_json(force=True)
        operation_handlers = {
            'water': self.logic_wrapper.water_pot,
            'delete': self.logic_wrapper.delete_pot
        }
        ids = json['ids']
        operation_handler = operation_handlers[json['operation']]
        for i in ids:
            operation_handler(i)
        self.logic_wrapper.json_wrap.dump()


class Plants(Resource):
    def __init__(self):
        self.data = garden_logic.Plants()

    def get(self):
        return self.data


api.add_resource(Plants, '/plants/')
api.add_resource(Pots, '/pots/')

if __name__ == '__main__':
    app.run(debug=True)
