import Type as type

class Token:
    def __init__(self, type, lexem, line):
        self.type = type
        self.lexem = lexem
        self.line = line
     
    