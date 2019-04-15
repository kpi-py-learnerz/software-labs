from garden_data import GardenData

garden_data = GardenData('plants.json', 'pots.json')


class Pots:
    """
    Class-wrapper for business logic.
    """

    FIELDS = ["plant", "water-percentage", "pot-size"]

    def __init__(self):
        self.json_wrap = garden_data.pots

    def delete_single(self, i):
        """
        Deletes single pot
        :param i: index
        :return:
        """
        del self.json_wrap.data['pots'][i]

    def delete(self, data):
        """
        Deletes all pots designated by data
        :param data: list of indices
        :return:
        """
        for i in data:
            self.delete_single(i)

    def water_single(self, i):
        """
        Waters single pot
        :param i:
        :return:
        """
        self.json_wrap.data['pots'][i]['water-percentage'] = '100'

    def water(self, data):
        """
        Waters all pots designated by data
        :param data: list of indices
        :return:
        """
        for i in data:
            self.water_single(i)

    def add(self, data):
        """
        Adds a pot
        :param data: pot
        :return:
        """
        new_data = {}
        try:
            for k in self.FIELDS:
                new_data[k] = data[k]
        except KeyError:
            return 404
        self.json_wrap.data['pots'].append(new_data)

    def update(self, i, data):
        """
        Updates a pot
        :param i: index
        :param data: pot
        :return:
        """
        try:
            for k, v in data:
                self.json_wrap.data['pots'][i][self.FIELDS[self.FIELDS.index(k)]] = v
                # self.json_wrap.data['pots'][i][k] = v
        except KeyError:
            return 404


class Plants:
    """
    Class-wrapper for business logic.
    """
    def __init__(self):
        self.json_wrap = garden_data.plants

    def add(self, data):
        """
        Adds a plant
        :param data: plant
        :return:
        """
        self.json_wrap.data['plants'].append(data)
