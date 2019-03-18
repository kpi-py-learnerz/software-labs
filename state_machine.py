

def find_what_to_do_next(menu, choice):
    """
    Finds function do by field choice in dict menu.
    When not found, ValueError raises
    :param menu: dict
    :param choice: dict field 'input'
    :return: found dict field 'do'
    >>> def s1(): pass
    >>> def s2(): pass
    >>> s1 == find_what_to_do_next([{'prompt': 'list all plants', 'input': '1', 'do': s1},\
                                    {'prompt': 'water plants', 'input': '2', 'do': s1},\
                                    {'prompt': 'quit', 'input': 'q', 'do': s2}],\
                                    '1')
    True
    >>> s1 == find_what_to_do_next([{'prompt': 'list all plants', 'input': '1', 'do': s1},\
                                    {'prompt': 'water plants', 'input': '2', 'do': s1},\
                                    {'prompt': 'quit', 'input': 'q', 'do': s2}],\
                                    'e')
    Traceback (most recent call last):
        ...
    ValueError: can't find 'e' in menu
    """
    for option in menu:
        if choice == option['input']:
            return option['do']
    raise ValueError("can't find '%s' in menu" % choice)


def print_options(menu, file=None):
    """
    Prints menu options to file
    :param menu: sequence of options, specified by a dict
    :param file: output stream; a file-like object (stream); defaults to the current sys.stdout.
    :return: None
    >>> print_options([{'prompt': 'list all plants', 'input': '1', 'do': s1},\
                       {'prompt': 'water plants', 'input': '2', 'do': s1},\
                       {'prompt': 'quit', 'input': 'q', 'do': s2}])
    1 to list all plants
    2 to water plants
    q to quit
    """
    for option in menu:
        print(option['input'] + ' to ' + option['prompt'], file=file)


def prompt_menu(menu, scan=__builtins__.input):
    """
    Gathers option from user to decide which function call next
    :param menu:
    :param scan:
    :return: the function which is to be called next
    >>> def s1(): pass
    >>> def s2(): pass
    >>> class UserInp:
    ...     def __init__(self, inp): self.inp = inp
    ...     def scan(self):
    ...         result = self.inp[0]
    ...         self.inp = self.inp[1:]
    ...         return result
    >>> def make_scanner(u_inp): return lambda: u_inp.scan()
    >>> s2 == prompt_menu([{'prompt': 'list all plants', 'input': '1', 'do': s1},\
                           {'prompt': 'water plants', 'input': '2', 'do': s1},\
                           {'prompt': 'quit', 'input': 'q', 'do': s2}],\
                           scan=make_scanner(UserInp(['e', 'k', 'q'])))
    Enter:
    1 to list all plants
    2 to water plants
    q to quit
    Sorry, try again
    Sorry, try again
    True
    """
    print("Enter:")
    print_options(menu)
    while True:
        choice = str(scan())
        try:
            return find_what_to_do_next(menu, choice)
        except ValueError:
            print("Sorry, try again")


def s1():
    print("s1")


def s2():
    print("s2")


menu1 = [
    {'prompt': 'list all plants', 'input': '1', 'do': s1},
    {'prompt': 'water plants', 'input': '2', 'do': s1},
    {'prompt': 'quit', 'input': 'q', 'do': s2}
]
prompt_menu(menu1)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
