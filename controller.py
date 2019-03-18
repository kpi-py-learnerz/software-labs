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
