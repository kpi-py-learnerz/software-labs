import json
from flask import request
from controller import Controller
from PyInquirer import Separator

SERVER_IP = "http://127.0.0.1:5000/"
controller = Controller()


questions = [
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


def is_quit(choice):
    return choice == 'q'


def main():
    while True:
        prompt = {}
        choice = json.dumps(controller.scan(prompt))
        # if is_quit(choice):
        #     break
        # response = request.post(SERVER_IP, json=choice).json()
        # controller.print(response)
    else:
        controller.print("Quitting...")


if __name__ == '__main__':
    main()
