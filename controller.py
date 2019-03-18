# Packages for pretty printing
from clint.arguments import Args
from clint.textui import puts, colored, indent
# Or that one
import PyInquirer

import state_machine


class Controller:
    def scan(self, prompt):
        input(prompt)

    def print(self, what):
        print(what)
