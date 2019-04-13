from __future__ import print_function, unicode_literals
from PyInquirer import style_from_dict, Token, prompt, Separator
from pprint import pprint
import requests


style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: '',
})


def make_question(question_type, message, name, choices):
    return {'type': question_type, 'message': message,
            'name': name, 'choices': choices}


def option_value_dict_to_question(question_type, message, name, option_value_dict):
    choices = [{'name': key, 'value': value} for key, value in option_value_dict.items()]
    return make_question(question_type, message, name, choices)


def dict_to_pretty_str(d):
    return ', '.join('%s: %s' % (k, v) for k, v in d.items())


def dict_list_to_multi_select_question(message, name, dict_list):
    choices, i = [], 0
    for d in dict_list:
        choices.append({'name': dict_to_pretty_str(d), 'value': i})
        i += 1
    question = make_question('checkbox', message, name, choices)
    return question


class ResourceClient:
    def __init__(self, uri, json_key):
        self.uri = uri
        self.json_key = json_key

    def get(self):
        return requests.get(self.uri).json()[self.json_key]

    def print(self):
        # TODO the printer
        resource = self.get()
        print(resource)

    def post(self, json_maker):
        self.print()
        response = requests.post(self.uri, json=json_maker())
        # self._print_water_response(water_response)
        self.print()


class GardenClient:
    SERVER_IP = "http://127.0.0.1:5000"  # note here's no slash

    def __init__(self):
        self.pots_resource = ResourceClient(self.SERVER_IP + '/pots/', 'pots')
        self.plants_resource = ResourceClient(self.SERVER_IP + '/plants/', 'plants')
        self.option_function_dict = {
            'Полити вазон': self.water_pot,
            'Додати вазон': self.add_pot,
            'Видалити вазон': self.delete_pot
        }
        message = 'Виберіть операцію'
        self.operation_key = 'operation'
        self.questions = [
            option_value_dict_to_question('list', message, self.operation_key, self.option_function_dict)
        ]

    @staticmethod
    def _print_pots(pots):
        # TODO the printer
        pprint(pots)

    def print_all_pots(self):
        pots = self.pots_resource.get()
        self._print_pots(pots)

    @staticmethod
    def _make_post_json(operation, ids):
        return {'operation': operation, 'ids': ids}

    def _prompt_post_json(self, operation, resource_name):
        pots = self.pots_resource.get()
        question_message = 'Виберіть хоча б 1 %s' % resource_name
        questions = [dict_list_to_multi_select_question(question_message, 'pots', pots)]
        ids = prompt(questions)
        while len(ids['pots']) == 0:
            ids = prompt(questions)
        print(ids)
        return self._make_post_json(operation, ids['pots'])

    def water_pot(self):
        self.pots_resource.post(lambda: self._prompt_post_json('water', 'вазон'))

    def add_pot(self):
        pass

    def delete_pot(self):
        self.pots_resource.post(lambda: self._prompt_post_json('delete', 'вазон'))

    def prompt(self):
        operation = prompt(self.questions)[self.operation_key]
        operation()


def dict_item_to_str(dict_item):
    return ", ".join(["%s: %s" % (k, v) for k, v in dict_item.items()])


def main():
    garden_client = GardenClient()
    while True:
        garden_client.prompt()


if __name__ == '__main__':
    main()
