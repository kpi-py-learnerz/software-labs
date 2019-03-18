import json
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
