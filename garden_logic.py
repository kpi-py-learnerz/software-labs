from garden_data import GardenData

garden_data = GardenData('plants.json', 'pots.json')


class Pots:
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
        self.json_wrap.data['pots'].append(data)

    def update(self, i, data):
        # TODO
        pass


class Plants:
    def __init__(self):
        self.json_wrap = garden_data.plants

    def add(self, data):
        self.json_wrap.data['plants'].append(data)