from garden_data import GardenData

garden_data = GardenData('plants.json', 'pots.json')


class Pots:
    def __init__(self):
        self.json_wrap = garden_data.pots

    def delete_pot(self, i):
        del self.json_wrap.data['pots'][i]

    def water_pot(self, i):
        self.json_wrap.data['pots'][i]['water-percentage'] = '100'


class Plants:
    def __init__(self):
        pass