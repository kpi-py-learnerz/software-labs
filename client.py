from __future__ import print_function, unicode_literals
from PyInquirer import style_from_dict, Token, prompt
from terminaltables import SingleTable
import requests


def safe_prompt(questions):
    style = style_from_dict({
        Token.Separator: '#cc5454',
        Token.QuestionMark: '#673ab7 bold',
        Token.Selected: '#cc5454',  # default
        Token.Pointer: '#673ab7 bold',
        Token.Instruction: '',  # default
        Token.Answer: '#f44336 bold',
        Token.Question: '',
    })
    answer = prompt(questions, style=style)
    if answer == {}:
        raise KeyboardInterrupt
    else:
        return answer


def make_question(question_type, message, name, choices):
    return {'type': question_type, 'message': message,
            'name': name, 'choices': choices}


def option_value_dict_to_question(question_type, message, name, option_value_dict):
    choices = [{'name': key, 'value': value} for key, value in option_value_dict.items()]
    return make_question(question_type, message, name, choices)


def dict_to_pretty_str(d):
    return ', '.join('%s: %s' % (k, v) for k, v in d.items())


def dict_list_to_multi_select_question(question_type, message, name, dict_list):
    choices, i = [], 0
    for d in dict_list:
        choices.append({'name': dict_to_pretty_str(d), 'value': i})
        i += 1
    question = make_question(question_type, message, name, choices)
    return question


class ResourceClient:
    def __init__(self, uri, json_key):
        self.uri = uri
        self.json_key = json_key

    def get(self):
        return requests.get(self.uri).json()[self.json_key]

    def put(self):
        """

        :return:
        """
        pass

    def delete(self):
        """

        :return:
        """
        pass

    def print(self):
        resource = self.get()
        # print(resource)
        attribute_names = tuple(k for k, v in resource[0].items())
        rows = [tuple(row[attribute_name] for attribute_name in attribute_names) for row in resource]
        t_table = SingleTable([attribute_names] + rows)
        print(t_table.table)

    def post(self, json_maker):
        self.print()
        response = requests.post(self.uri, json=json_maker())
        # self._print_water_response(water_response)
        self.print()


def validate_str(value): return len(value.split()) != 0


def validate_unsigned(value):
    try:
        return int(value) >= 0
    except ValueError:
        return False


def validate_percentage(value):
    return validate_unsigned(value) and int(value) <= 100


def capitalize_all_words(val):
    return ' '.join([word.capitalize() for word in val.split()])


class GardenClient:
    SERVER_IP = "http://127.0.0.1:5000"  # note here's no slash

    def __init__(self):
        self.pots_resource = ResourceClient(self.SERVER_IP + '/pots/', 'pots')
        self.plants_resource = ResourceClient(self.SERVER_IP + '/plants/', 'plants')
        self.option_function_dict = {
            'Полити вазон': self.water_pot,
            'Додати вазон': self.add_pot,
            'Видалити вазон': self.delete_pot,
            'Вийти': lambda: 'quit'
        }
        message = 'Виберіть операцію'
        self.operation_key = 'operation'
        self.questions = [
            option_value_dict_to_question('list', message, self.operation_key, self.option_function_dict)
        ]

    @staticmethod
    def _make_post_json(operation, data):
        return {'operation': operation, 'data': data}

    def _prompt_selection_post_json(self, selection_type, operation, resource_name):
        pots = self.pots_resource.get()
        message_formats = {
            'checkbox': 'Виберіть хоча б 1 %s',
            'list': 'Виберіть %s'
        }
        question_message = message_formats[selection_type] % resource_name
        questions = [dict_list_to_multi_select_question(selection_type, question_message, 'pots', pots)]
        ids = safe_prompt(questions)
        while len(ids['pots']) == 0:
            ids = safe_prompt(questions)
        # print(ids)
        return self._make_post_json(operation, ids['pots'])

    def water_pot(self):
        self.pots_resource.post(lambda: self._prompt_selection_post_json('checkbox', 'water', 'вазон'))

    def _prompt_plant(self):
        message_format = 'Введіть %s'
        input_plant_questions = [
            {
                'type': 'input',
                'name': 'name',
                'message': message_format % "ім'я рослини",
                'validate': validate_str,
                'filter': capitalize_all_words
            },
            {
                'type': 'input',
                'name': "watering-period",
                'message': message_format % "період поливу",
                'validate': validate_unsigned,
                'filter': str
            },
            {
                'type': 'input',
                'name': "water-amount-per-cubic-decimeter",
                'message': message_format % "кількість води на дм^3",
                'validate': validate_unsigned,
                'filter': str
            }
        ]
        plant = safe_prompt(input_plant_questions)
        return self._make_post_json('add', plant)

    def _prompt_pot(self):
        plants = self.plants_resource.get()
        select_question = dict_list_to_multi_select_question('list', 'Виберіть рослину', 'plant', plants)
        select_question['choices'].insert(0, {'name': 'Нова рослина', 'value': 'new'})
        selected_plant_answer = safe_prompt(select_question)
        if selected_plant_answer['plant'] == 'new':
            self.plants_resource.post(self._prompt_plant)
            # print(self.plants_resource.get())
            plant_id = len(plants)  # dangerous code, reconsider
        else:
            plant_id = selected_plant_answer['plant']
        plants = self.plants_resource.get()
        pot_plant_name = plants[plant_id]['name']
        message_format = 'Введіть %s'
        input_pot_questions = [
            {
                'type': 'input',
                'name': 'water-percentage',
                'message': message_format % "поточний стан поливу (%)",
                'validate': validate_percentage,
                'filter': str
            },
            {
                'type': 'input',
                'name': 'pot-size',
                'message': message_format % "розмір горщика",
                'validate': validate_unsigned,
                'filter': str
            }
        ]
        new_pot = safe_prompt(input_pot_questions)
        new_pot['plant'] = pot_plant_name
        return self._make_post_json('add', new_pot)

    def add_pot(self):
        self.pots_resource.post(self._prompt_pot)

    """
    def _prompt_update_pot(self):
        selected_json =  self._prompt_selection_post_json('checkbox', 'water', 'вазон')
        ids = selected_json['ids']
        for i in ids:
            self.pots_resource.post(lambda: self._prompt_selection_post_json('checkbox', 'delete', 'вазон'))

    def update_pot(self):
        self.pots_resource.post(self._prompt_update_pot)
    """

    def delete_pot(self):
        self.pots_resource.post(lambda: self._prompt_selection_post_json('checkbox', 'delete', 'вазон'))

    def prompt(self):
        operation = safe_prompt(self.questions)[self.operation_key]
        answer = operation()
        # print(answer)
        return answer


def dict_item_to_str(dict_item):
    return ", ".join(["%s: %s" % (k, v) for k, v in dict_item.items()])


class Main:
    def __init__(self):
        self.garden_client = GardenClient()

    def main_menu(self):
        try:
            final_answer = self.garden_client.prompt()
        except KeyboardInterrupt:
            print("Ввід відмінено користувачем, вихід в головне меню")
            return None
        else:
            return final_answer

    def run(self):
        while self.main_menu() != 'quit':
            pass


if __name__ == '__main__':
    main = Main()
    main.run()
