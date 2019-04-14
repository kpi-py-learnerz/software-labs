import json


class JsonData:
    def __init__(self, path):
        self.path = path
        with open(path) as stream:
            self.data = json.load(stream)

    def dump(self):
        with open(self.path, "w", encoding='utf-8') as gfp:
            json.dump(self.data, gfp, indent=True)


class GardenData:
    def __init__(self, plants_path, pots_path):
        self.plants = JsonData(plants_path)
        self.pots = JsonData(pots_path)

    def dump(self):
        self.plants.dump()
        self.pots.dump()
