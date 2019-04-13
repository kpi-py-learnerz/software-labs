from flask import Flask, request
from flask_restful import Resource, Api
from garden_data import GardenData
import garden_logic

app = Flask(__name__)
api = Api(app)
garden_data = GardenData('plants.json', 'garden.json')


class Pots(Resource):
    def __init__(self):
        self.data = garden_data.pots

    def get(self):
        return self.data

    def post(self):
        json = request.get_json(force=True)
        # TODO: something about this json using garden_logic
        print(json)


class Plants(Resource):
    def __init__(self):
        self.data = garden_data.plants

    def get(self):
        return self.data


api.add_resource(Plants, '/plants/')
api.add_resource(Pots, '/pots/')
# TODO: more resources to perform business logic

if __name__ == '__main__':
    app.run(debug=True)
