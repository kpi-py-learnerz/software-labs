# Packages for pretty printing
from __future__ import print_function, unicode_literals
from PyInquirer import style_from_dict, Token, prompt, Separator


class Controller:
    def __init__(self):
        self.style = style_from_dict({
            Token.Separator: '#cc5454',
            Token.QuestionMark: '#673ab7 bold',
            Token.Selected: '#cc5454',  # default
            Token.Pointer: '#673ab7 bold',
            Token.Instruction: '',  # default
            Token.Answer: '#f44336 bold',
            Token.Question: '',
        })

    def scan(self, questions):
        return prompt(questions, style=self.style)


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
