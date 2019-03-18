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


start_q = [
    {
        'type': 'checkbox',
        'message': 'Select plants',
        'name': 'plants',
        'choices': [
            Separator('= Оберіть операцію ='),
            {
                'name': 'Вивести стан всіх квіток'
            },
            {
                'name': 'Вийти'
            }
        ],
        'validate': lambda answer: 'You must choose at least one topping.' \
            if len(answer) == 0 else True
    }
]

state_q = [
    {
        'type': 'checkbox',
        'message': 'Select toppings',
        'name': 'toppings',
        'choices': [
            Separator('= Оберіть операцію ='),
            {
                'name': 'Полити квіти'
            },
            {
                'name': 'Додати квітку'
            },
            {
                'name': 'Видалити квітку'
            },
            {
                'name': 'Вийти'
            }
        ],
        'validate': lambda answer: 'You must choose at least one topping.' \
            if len(answer) == 0 else True
    }
]


def dict_item_to_str(dict_item):
    return ", ".join(["%s: %s" % (k, v) for k, v in dict_item.items()])


class Option:
    """
    Simple PyInquirer option wrapper
    """
    def __init__(self, option):
        self.option = option
        self.str = dict_item_to_str(self.option)

    def split(self, c):
        return self.str.split(c)


def dict_list_to_option_list(dict_list):
    return [{"name": Option(dict_item)} for dict_item in dict_list]


def option_list_to_menu(menu_head, option_list):
    plants_menu = [Separator(menu_head)]
    plants_menu = plants_menu + option_list
    return [
        {
            'type': 'checkbox',
            'message': 'Select plants',
            'name': 'plants',
            'choices': plants_menu,
            'validate': lambda answer: 'You must choose at least one option.'
                if len(answer) == 0 else True
        }
    ]


SERVER_IP = "http://127.0.0.1:5000"  # note here's no slash


def get_request(sub_uri=''):
    return requests.get(SERVER_IP + sub_uri)


def main():
    while True:
        response = get_request('/garden/')
        # response = get_request('/plants/')
        response_json = response.json()
        option_list = dict_list_to_option_list(response_json['pots'])
        menu = option_list_to_menu('= Оберіть горщик =', option_list)
        choice = prompt(menu, style=style)
        pprint(choice)
        if not True:
            break
    else:
        print("Quitting...")


if __name__ == '__main__':
    main()

# answers = prompt(questions, style=style)
# pprint(answers)

"""

class Controller:
    def scan(self, questions):
        self.answers = prompt(questions, style=style)

    def print(self, what):
        pprint(self.answers)

"""