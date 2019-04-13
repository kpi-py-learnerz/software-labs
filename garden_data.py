import json


class JsonData:
    def __init__(self, path):
        with open(path) as stream:
            self.data = json.load(stream)


class GardenData:
    def __init__(self, plants_path, garden_path):
        self.plants = JsonData(plants_path).data
        self.pots = JsonData(garden_path).data
