from os import path
import Token as token
import Type as type
class Scanner:
    fileName = None
    file = None
    def __init__(self, fileName):
        self.type = type.Type()
        self.fileName = fileName
        self.reservedWords = { 
            'inteiro': self.type.INTEIRO,
            'real': self.type.REAL, 
            'logico': self.type.LOGICO,
            'character': self.type.charACTER,
            'se': self.type.SE,
            'senao': self.type.SENAO,
            'enquanto': self.type.ENQUANTO,
            'leia': self.type.LEIA,
            'escreva': self.type.ESCREVA,
            'falso': self.type.FALSO,
            'verdadeiro': self.type.VERDADEIRO
        }
    
    def open_file(self):
        if (self.file is not None):
            return 'File already is open'
        elif path.exists(self.fileName):
            self.file = open(self.file, 'r')
            self.buffer = ''
            self.line = 1
            return 'Ok'
        else:
            return 'File not found'
            quit()
    
    def close_file(self):
        if (self.file is None):
            return "There isn't open file"
            quit()
        else:
            self.file.close()
    
    def getChar(self):
        if self.file is None:
            print("There isn't open file")
            quit()
        elif len(self.buffer) > 0:
            c = self.buffer[0]
            self.buffer = self.buffer[1:]
            return c
        else:
            c = self.file.read(1)
            # se nao foi eof, pelo menos um char foi lido
            # senao len(c) == 0
            if len(c) == 0:
                return None
            else:
                return c.lower()

    def ungetChar(self, c):
        if not c is None:
            self.buffer = self.buffer + c

    def getToken(self):
        lexem = ''
        state = 1
        char = None
        while (True):
            if state == 1:
                # estado inicial que faz primeira classificacao
                char = self.getChar()
                if char is None:
                    return token(self.type.FIMARQ, '<eof>', self.line)
                elif char in {' ', '\t', '\n'}:
                    if char == '\n':
                        self.line = self.line + 1
                elif char.isalpha():
                    state = 2
                elif char.isdigit():
                    state = 3
                elif char in {':', ';', '+', '*', '(', ')', '{', '}', '>', '=', '<', '!', ',', '/', '-'}:
                    state = 4
                elif char == '#':
                    state = 5
                else:
                    return token(self.type.ERROR, '<' + char + '>', self.line)
            elif state == 2:
                # estado que trata nomes (identificadores ou palavras reservadas)
                lexem = lexem + char
                char = self.getChar()
                if char is None or (not char.isalnum()):
                    # terminou o nome
                    self.ungetChar(char)
                    if lexem in self.reservedWords:
                            return token(self.reservedWords[lexem], lexem, self.line)
                    else:
                        return token(self.type.ID, lexem, self.line)
            elif state == 3:
                # estado que trata numeros inteiros
                lexem = lexem + char
                char = self.getChar()
                if char is None or (not char.isdigit()) or char is '.':
                    # terminou o numero
                    self.ungetChar(char)
                    return token(self.type.CTE, lexem, self.line)
            elif state == 4:
                # estado que trata outros tokens primitivos comuns
                lexem = lexem + char
                if char == '=':
                    return token(self.type.ATRIB, lexem, self.line)
                elif char == ';':
                    return token(self.type.PTOVIRG, lexem, self.line)
                elif char == '+':
                    return token(self.type.ADI, lexem, self.line)
                elif char == '*':
                    return token(self.type.MULT, lexem, self.line)
                elif char == '(':
                    return token(self.type.ABREPAR, lexem, self.line)
                elif char == ')':
                    return token(self.type.FECHAPAR, lexem, self.line)
                elif char == '{':
                    return token(self.type.ABRECH, lexem, self.line)
                elif char == '}':
                    return token(self.type.FECHACH, lexem, self.line)
            elif state == 5:
                # consumindo comentario
                while (not char is None) and (char != '\n'):
                    char = self.getChar()
                self.ungetChar(char)
                state = 1