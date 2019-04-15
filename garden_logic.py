from garden_data import GardenData

garden_data = GardenData('plants.json', 'pots.json')


class Pots:
    FIELDS = ["plant", "water-percentage", "pot-size"]

    def __init__(self):
        self.json_wrap = garden_data.pots

    def delete_single(self, i):
        del self.json_wrap.data['pots'][i]

    def delete(self, data):
        for i in data:
            self.delete_single(i)

    def water_single(self, i):
        self.json_wrap.data['pots'][i]['water-percentage'] = '100'

    def water(self, data):
        for i in data:
            self.water_single(i)

    def add(self, data):
        new_data = {}
        try:
            for k in self.FIELDS:
                new_data[k] = data[k]
        except KeyError:
            return 404
        self.json_wrap.data['pots'].append(new_data)

    def update(self, i, data):
        try:
            for k, v in data:
                self.json_wrap.data['pots'][i][self.FIELDS[self.FIELDS.index(k)]] = v
                # self.json_wrap.data['pots'][i][k] = v
        except KeyError:
            return 404


class Plants:
    def __init__(self):
        self.json_wrap = garden_data.plants

    def add(self, data):
        self.json_wrap.data['plants'].append(data)
