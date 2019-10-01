import Scanner as scanner
import Type as Type
import Token as token
class Parser:
    simbol_table = None
    def __init__(self):
        self.simbol_table = dict()
        self.scanner = scanner.Scanner()

    def consume_token(self):
        token = self.scanner.getToken()