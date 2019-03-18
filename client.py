from __future__ import print_function, unicode_literals

"""import json
from flask import request
from controller import Controller

SERVER_IP = "http://127.0.0.1:5000/"
controller = Controller()


def is_quit(choice):
    return choice == 'q'


def main():
    while True:
        prompt = {}
        choice = json.dumps(controller.scan(prompt))
        if is_quit(choice):
            break
        response = request.post(SERVER_IP, json=choice).json()
        controller.print(response)
    else:
        controller.print("Quitting...")

if __name__ == '__main__':
    main()
"""
import json
SERVER_IP = "http://127.0.0.1:5000/"


# Packages for pretty printing

from PyInquirer import style_from_dict, Token, prompt, Separator
from pprint import pprint


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


def plant_to_str(plant):
    return ", ".join(["%s: %s" % (k, v) for k, v in plant.items()])


class PlantOption:
    """
    Simple plant wrapper
    """
    def __init__(self, plant):
        self.plant = plant
        self.str = plant_to_str(self.plant)

    def split(self, c):
        return self.str.split(c)


def pots_to_questions(json):
    return [{"name": PlantOption(plant)} for plant in json]


def plants_options_to_menu(plants_options):
    plants_menu = [Separator('= Оберіть рослину =')]
    plants_menu = plants_menu + plants_options
    return [
        {
            'type': 'checkbox',
            'message': 'Select plants',
            'name': 'plants',
            'choices': plants_menu,
            'validate': lambda answer: 'You must choose at least one topping.' \
                if len(answer) == 0 else True
        }
    ]

"""plants = {
  "time": {
    "min": "10",
    "hour": "10",
    "date": {
      "day": "0",
      "month": "0",
      "year": "1970"
    }
  },
  "pots": [
    {
      "plant": "Cactuss",
      "water-percentage": "100",
      "pot-size": "999"
    },
    {
      "plant": "Cactus",
      "water-percentage": "100",
      "pot-size": "999"
    },
    {
      "plant": "Ficus",
      "water-percentage": "100",
      "pot-size": "999"
    },
    {
      "plant": "Lily",
      "water-percentage": "100",
      "pot-size": "999"
    },
    {
      "plant": "Rose",
      "water-percentage": "100",
      "pot-size": "999"
    }
  ]
}
"""

import requests
def main():
    while True:
        choice = 1;
        response = requests.post(SERVER_IP, json={})

        questions = plants_options_to_menu(pots_to_questions(response.json()))
        choice = prompt(questions, style=style)
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