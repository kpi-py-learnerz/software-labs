from __future__ import print_function, unicode_literals
from PyInquirer import style_from_dict, Token, prompt
from terminaltables import SingleTable
import requests


def safe_prompt(questions):
    """
    Asks the user the questions.
    :param questions:
    :return : Answer
    if KeyboardInterrupt occurred raises KeyboardInterrupt.
    """
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
    """
    Makes question from params.
    :param question_type:
    :param message:
    :param name:
    :param choices:
    :return: Question dict.
    """
    return {'type': question_type, 'message': message,
            'name': name, 'choices': choices}


def option_value_dict_to_question(question_type, message, name, option_value_dict):
    """
    Transforms value dict to question.
    :param question_type:
    :param message:
    :param name:
    :param option_value_dict:
    :return: Question dict.
    """
    choices = [{'name': key, 'value': value} for key, value in option_value_dict.items()]
    return make_question(question_type, message, name, choices)


def dict_to_pretty_str(d):
    """
    Transforms dictionary to one string
    :param d: dict object
    :return: string
    """
    return ', '.join('%s: %s' % (k, v) for k, v in d.items())


def dict_list_to_multi_select_question(question_type, message, name, dict_list):
    """
    Transforms list of dict to multiple select question.
    :param question_type:
    :param message:
    :param name:
    :param dict_list:
    :return: Question.
    """
    choices, i = [], 0
    for d in dict_list:
        choices.append({'name': dict_to_pretty_str(d), 'value': i})
        i += 1
    question = make_question(question_type, message, name, choices)
    return question


class ResourceClient:
    """
    Class-wrapper for communicating with server resources
    """
    def __init__(self, uri, json_key):
        """
        ResourceClient constructor
        :param uri: URL of resource json
        :param json_key: Key for resource in retrieved json
        """
        self.uri = uri
        self.json_key = json_key

    def get(self):
        """
        Retrievers resource.
        :return:
        """
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
        """
        Prints pretty table designated by resource.
        :return: None
        """
        resource = self.get()
        # print(resource)
        attribute_names = tuple(k for k, v in resource[0].items())
        rows = [tuple(row[attribute_name] for attribute_name in attribute_names) for row in resource]
        t_table = SingleTable([attribute_names] + rows)
        print(t_table.table)

    def post(self, json_maker):
        """
        Makes post request.
        :param json_maker: function that makes a json for post request.
        :return: None
        """
        self.print()
        response = requests.post(self.uri, json=json_maker())
        # self._print_water_response(water_response)
        self.print()


def validate_str(value):
    """
    Validates string.
    :param value:
    :return: bool
    """
    return len(value.split()) != 0


def validate_unsigned(value):
    """
    Validates integer to be not negative
    :param value:
    :return: bool
    """
    try:
        return int(value) >= 0
    except ValueError:
        return False


def validate_percentage(value):
    """
    Validates unsigned to be <= than 100.
    :param value:
    :return: bool
    """
    return validate_unsigned(value) and int(value) <= 100


def capitalize_all_words(val):
    """
    Capitalizes all words.
    :param val:
    :return: resulting string
    """
    return ' '.join([word.capitalize() for word in val.split()])


class GardenClient:
    """
    Class-wrapper to communicate with plants & pots resources from server
    """
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
        """
        Creates json to be passed by post request
        :param operation:
        :param data:
        :return: post json
        """
        return {'operation': operation, 'data': data}

    def _prompt_selection_post_json(self, selection_type, operation, resource_name):
        """
        Asks user to choose ids or single id of resource of pot.
        :param selection_type:
        :param operation:
        :param resource_name:
        :return:
        """
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
        """
        Waters pots. Asks pots and then sends request for watering them
        :return:
        """
        self.pots_resource.post(lambda: self._prompt_selection_post_json('checkbox', 'water', 'вазон'))

    def _prompt_plant(self):
        """
        Asks users to input plant data fields
        :return: post json
        """
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
        """
        Asks users to input pot data fields
        :return: post json
        """
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
        """
        Sends request to add a pot
        :return: None
        """
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
        """
        Sends request to delete a pot
        :return: None
        """
        self.pots_resource.post(lambda: self._prompt_selection_post_json('checkbox', 'delete', 'вазон'))

    def prompt(self):
        """
        Asks the user for operation applied to garden resource.
        :return: answer if may return 'quit'
        """
        operation = safe_prompt(self.questions)[self.operation_key]
        answer = operation()
        # print(answer)
        return answer


class Main:
    """
    Main menu wrapper.
    """
    def __init__(self):
        self.garden_client = GardenClient()

    def main_menu(self):
        """
        Prompts main menu.
        :return: May return 'quit'
        """
        try:
            final_answer = self.garden_client.prompt()
        except KeyboardInterrupt:
            print("Ввід відмінено користувачем, вихід в головне меню")
            return None
        else:
            return final_answer

    def run(self):
        """
        While not 'quit' prompts main menu.
        :return:
        """
        while self.main_menu() != 'quit':
            pass


if __name__ == '__main__':
    main = Main()
    main.run()
