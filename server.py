from flask import Flask, request, Response
from flask_restful import Resource, Api
import garden_logic

app = Flask(__name__)
api = Api(app)


class Pots(Resource):
    """
    Class-wrapper for pots resources.
    """
    def __init__(self):
        self.logic_wrapper = garden_logic.Pots()

    def get(self):
        """
        Sends resource to client.
        :return:
        """
        return self.logic_wrapper.json_wrap.data

    def post(self):
        """
        Does needed operation on resource on pot
        :return:
        """
        json = request.get_json(force=True)
        operation_handlers = {
            'water': self.logic_wrapper.water,
            'delete': self.logic_wrapper.delete,
            'add': self.logic_wrapper.add
        }
        try:
            data = json['data']
            operation_handler = operation_handlers[json['operation']]
        except KeyError:
            return 404
        operation_handler(data)
        self.logic_wrapper.json_wrap.dump()


class Plants(Resource):
    """
    Class-wrapper for plants resources
    """
    def __init__(self):
        self.logic_wrapper = garden_logic.Plants()

    def get(self):
        """
        Sends resource to client.
        :return:
        """
        return self.logic_wrapper.json_wrap.data

    def post(self):
        """
        Does needed operation on resource on plant
        :return:
        """
        json = request.get_json(force=True)
        operation_handlers = {
            'add': self.logic_wrapper.add
        }
        try:
            data = json['data']
            operation_handler = operation_handlers[json['operation']]
        except KeyError:
            return 404
        operation_handler(data)
        self.logic_wrapper.json_wrap.dump()


api.add_resource(Plants, '/plants/')
api.add_resource(Pots, '/pots/')

if __name__ == '__main__':
    """
    Currently the server supports the following requests:
        on URI '/':
            GET 
            -> response is plaintext 'index.html'
        on URI '/plants/':
            GET 
            -> JSON with array of <plant-json>s
            POST 
            + JSON with following format:
                {
                    'operation': 'add',
                    'data': <plant-json>
                }
            -> adds the plant to 'plants.json'
        on URI '/pots/':
            GET 
            -> JSON with array of <pot-json>s
            POST
            + JSON with following format:
                 {
                    'operation': <'water' or 'delete'>,
                    'data': <[int*]>
                 }
            -> 
            POST
            + JSON with following format:
                 {
                    'operation': 'add',
                    'data': <pot-json>
                 }
            -> adds the pot to 'pots.json'
    <pot-json> ->
    {
       "water-percentage": "<uint>",
       "pot-size": "<uint>",
       "plant": "<uchar*>"
    }
    <plant-json> ->
    {
        "name": "<uchar*>",
        "watering-period": "<uint>",
        "water-amount-per-cubic-decimeter": "<uint>"
    }        
    <uint> -> int > 0
    <uchar> -> unicode character (or utf-8, quite unsure)
    """
    app.run(debug=True)
