from flask import Flask, request, Response
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
    def __init__(self):
        self.logic_wrapper = garden_logic.Plants()

    def get(self):
        return self.logic_wrapper.json_wrap.data

    def post(self):
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


class IndexPage(Resource):
    INDEX_PATH = 'index.html'

    def __init__(self):
        with open(self.INDEX_PATH, encoding='utf-8') as html_stream:
            line_list = html_stream.readlines()
            self.file_str = ''.join(line_list)

    def get(self):
        resp = Response(self.file_str, mimetype='text/html')
        resp.status_code = 200
        return resp


api.add_resource(Plants, '/plants/')
api.add_resource(Pots, '/pots/')
api.add_resource(IndexPage, '/')

if __name__ == '__main__':
    app.run(debug=True)
