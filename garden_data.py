import json


class JsonData:
    """
    Class-wrapper for json data
    """
    def __init__(self, path):
        """
        Loads a json from path
        :param path:
        """
        self.path = path
        with open(path) as stream:
            self.data = json.load(stream)

    def dump(self):
        """
        Dumps json data
        :return:
        """
        with open(self.path, "w", encoding='utf-8') as gfp:
            json.dump(self.data, gfp, indent=True)


class GardenData:
    """
    Class-wrapper for garden data
    """
    def __init__(self, plants_path, pots_path):
        """
        Loads both jsons
        :param plants_path:
        :param pots_path:
        """
        self.plants = JsonData(plants_path)
        self.pots = JsonData(pots_path)

    def dump(self):
        """
        Dumps both jsons
        :return:
        """
        self.plants.dump()
        self.pots.dump()
