from flask import Flask
from flask_restful import Resource, Api
from garden_data import GardenData

app = Flask(__name__)
api = Api(app)
garden_data = GardenData('plants.json', 'garden.json')


class Garden(Resource):
    def __init__(self):
        self.data = garden_data.garden

    def get(self):
        return self.data


class Plants(Resource):
    def __init__(self):
        self.data = garden_data.plants

    def get(self):
        return self.data


api.add_resource(Plants, '/plants/')
api.add_resource(Garden, '/garden/')

if __name__ == '__main__':
    app.run(debug=True)
