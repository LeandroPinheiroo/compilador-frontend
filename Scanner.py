########################################################################
# João Paulo de Souza    - 0035329                                     #
# Leandro Souza Pinheiro - 0015137                                     #
# Trabalho Compiladores  - Front-end do compilador para a linguagem P  #
# Data: 31/10/2019                                                     #
########################################################################

from os import path
import Token as token
import Type as type
import re
class Scanner:
    fileName = None
    file = None
    # construtor da classe do scanner onde são declaradas a varíaveis relacionadas a dicionario de palavras
    # reservadas e o arquivo a ser lido
    def __init__(self, fileName):
        self.line = 0
        self.type = type.Type()
        self.fileName = fileName
        self.reservedWords = { 
            'inteiro': self.type.INTEIRO,
            'real': self.type.REAL, 
            'logico': self.type.LOGICO,
            'caracter': self.type.CARACTER,
            'se': self.type.SE,
            'senao': self.type.SENAO,
            'enquanto': self.type.ENQUANTO,
            'leia': self.type.LEIA,
            'escreva': self.type.ESCREVA,
            'falso': self.type.FALSO,
            'verdadeiro': self.type.VERDADEIRO,
            'programa': self.type.PROGRAMA,
            'variaveis': self.type.VARIAVEIS,
            'cadeia': self.type.CADEIA
        }
    
    # método para abrir o arquivo a ser lido
    def open_file(self):
        # verifica se o arquivo já não está aberto
        if (self.file is not None):
            # se estiver, avisa que o arquivo já foi aberto
            return 'File already is open'
        # procura o nome do arquivo no caminho da arquivo
        elif path.exists(self.fileName):
            # caso encontre, abre o arquivo e seta as variaveis
            # que serão utlizados pelo scanner
            self.file = open(self.fileName, 'r', encoding='utf-8')
            self.buffer = ''
            self.line = 1
            # retorna ok
            return 'Ok'
        else:
            # caso entre nesse quer dizer que não encontrou o arquivo
            return 'File not found'
    
    # método para fechar o arquivo    
    def close_file(self):
        # se a variavel do arquivo já está vazia, quer dizer que o arquivo já está fechado
        # ou não há arquivo aberto
        if (self.file is None):
            # retorna aviso
            return "There isn't open file"
        else:
            # se houver arquivo aberto, finaliza ele
            self.file.close()
    
    # método para ler os caracteres no arquivo, caractere a caractere
    def getChar(self):
        # verifica se o arquivo está aberto
        if self.file is None:
            # se não estiver aberto retorna o erro
            return "There isn't open file"
        # caso o arquivo esteja aberto e o buffer esteja preenchido
        elif len(self.buffer) > 0:
            # pega a primeira posição do buffer
            c = self.buffer[0]
            # remove ele do buffer
            self.buffer = self.buffer[1:]
            # e retorna o caractere lido no buffer
            return c
        else:
            # caso não tenha nada no buffer
            # le um caractere no arquivo
            c = self.file.read(1)
            # se nao foi eof, pelo menos um char foi lido
            # senao len(c) == 0
            if len(c) == 0:
                return None
            else:
                # retorna o caractere em lower case
                return c.lower()

    # método para buscar um caractere anterior no buffer para que a leitura acompanha a verificação
    def ungetChar(self, c):
        # verifca se o caractere não está vazio
        if not c is None:
            # senão estiver, guarda o caractere novamente no buffer
            self.buffer = self.buffer + c
    # método para que define o tratamento para o token lido
    def getToken(self):
        lexem = ''
        state = 1
        char = None
        # fica lendo até definir como tratar o token
        while (True):
            if state == 1:
                # estado inicial que faz primeira classificacao
                char = self.getChar()
                # verificação para final de arquivo, caso não encontrou o proximo caractere
                if char is None:
                    # retorna o token do final de arquivo
                    return token.Token(self.type.FIMARQ, '<eof>', self.line)
                # em caso de espaço em branco, tabulação ou pula-linha
                elif char in {' ', '\t', '\n'}:
                    # verifica somente se é pula linho
                    if char == '\n':
                        self.line = self.line + 1
                # verifica se o caractere lido é um caractere alpha
                elif re.search("[a-zA-z]",char):
                    # se for vai para o estado dois, onde acontecerá o tratamento
                    state = 2
                # se o caractere lido for um digito(numero), vai para o estado 3, onde vai ser tratato
                # também
                elif char.isdigit():
                    state = 3
                # se for um caractere especial, vai para o estado 4 onde ele será tratado, atribuição, etc
                elif char in {';', '+', '*', '(', ')', '{', '}', '=', '!', ',', '-'}:
                    state = 4
                elif char in {':', '>', '<', '/','"'}:
                    state = 5
                else:
                    # por fim senão for nenhum destes, entra em estado de de erro
                    return token.Token(self.type.ERRO, '<' + char + '>', self.line)
            elif state == 2:
                # estado que trata nomes (identificadores ou palavras reservadas)
                lexem = lexem + char
                # pega o proximo caractere
                char = self.getChar()
                # verifica se o caractere é vazio ou é um número
                if char is None or not re.search("[A-Za-z0-9]",char):
                    # se for, terminou de pegar as letras
                    # assim da unget
                    self.ungetChar(char)
                    # verifica se palavra lida está nas palavras reservadas da linguagem
                    if lexem in self.reservedWords:
                        # se tiver, retorna o token desta palavra
                        return token.Token(self.reservedWords[lexem], lexem, self.line)
                    else:
                        # senão, retorna o token de id
                        return token.Token(self.type.ID, lexem, self.line)
            elif state == 3:
                # estado que trata numeros inteiros e flutuanetes
                lexem = lexem + char
                # pega o proximo caractere
                char = self.getChar()
                # veirifica se é vazio, ou se não é digito, ou seja, acabou o numero
                if char is None or ((not char.isdigit()) and char != '.'):
                    # terminou o numero
                    self.ungetChar(char)
                    return token.Token(self.type.CTE, lexem, self.line)
            elif state == 4:
                # estado que trata outros tokens primitivos comuns e simbolos especiais da linguagem
                lexem = lexem + char
                if char == '=':
                    return token.Token(self.type.IGUAL, lexem, self.line)
                elif char == ';':
                    return token.Token(self.type.PVIRG, lexem, self.line)
                elif char == ',':
                    return token.Token(self.type.VIRG, lexem, self.line)
                elif char == '+':
                    return token.Token(self.type.OPAD, lexem, self.line)
                elif char == '*':
                    return token.Token(self.type.OPMUL, lexem, self.line)
                elif char == '-':
                    return token.Token(self.type.OPAD, lexem, self.line)
                elif char == '!':
                    return token.Token(self.type.OPNEG, lexem, self.line)
                elif char == '(':
                    return token.Token(self.type.ABREPAR, lexem, self.line)
                elif char == ')':
                    return token.Token(self.type.FECHAPAR, lexem, self.line)
                elif char == '{':
                    return token.Token(self.type.ABRECH, lexem, self.line)
                elif char == '}':
                    return token.Token(self.type.FECHACH, lexem, self.line)
            # estado para tratar os simbolos especiais que precisam de avaliação de mais de um char
            elif state == 5:
                if char == None:
                    lexem = 'um símbolo não compreendido pelo interpretador de arquivo'
                    return token.Token(self.type.ERRO,lexem,self.line)
                else:
                    lexem = lexem + char
                if char == '/':
                    char = self.getChar()
                    if (char == '*'):
                        char = self.getChar()
                        # comentario de bloco
                        while (not char is None):
                            # caso seja final de comentario de bloco, retorna o estado 1, indicando para verificar outras tokens
                            if (char == '*'):
                                char = self.getChar()
                                if (char == '/'):
                                    state = 1
                                    break
                            # vai pegando os caracteres até encontrar o fim de arquivo ou possivel final de bloco
                            # comentario
                            char = self.getChar()
                        #Zera lexama pois eh um comentario, onde o caractere que o representa esta sendo inserido na proxima leitura apos o comentario
                        lexem = ''
                    elif (char == '/'):
                        self.file.readline()
                        #while(char != '\n'):
                        #    char = self.getChar()
                        #    print(char)
                        #Zera lexama pois eh um comentario, onde o caractere que o representa esta sendo inserido na proxima leitura apos o comentario
                        lexem = ''
                        self.line += 1
                        state = 1
                        # comentario de linha
                    else:
                        # no caso da divisão
                        self.ungetChar(char)
                        return token.Token(self.type.OPMUL, lexem, self.line)
                elif (char == ':'):
                    char = self.getChar()
                    if (char == '='):
                        lexem = lexem + char
                        return token.Token(self.type.ATRIB, lexem, self.line)
                    else:
                        self.ungetChar(char)
                        return token.Token(self.type.DPONTOS,lexem,self.line)
                elif (char == '>'):
                    char = self.getChar()
                    if (char == '='):
                        lexem = lexem + char
                        return token.Token(self.type.OPREL, lexem, self.line)
                    else:
                        self.ungetChar(char)
                        return token.Token(self.type.OPREL, lexem, self.line)
                elif (char == '<'):
                    char = self.getChar()
                    if (char ==  '='):
                        lexem = lexem + char
                        return token.Token(self.type.OPREL,lexem,self.line)
                    elif (char == '>'):
                        lexem = lexem + char
                        return token.Token(self.type.OPREL,lexem,self.line)
                    else:
                        self.ungetChar(char)
                        return token.Token(self.type.OPREL,lexem,self.line)
                elif (char == '"'):
                    lexem = ''
                    char = self.getChar()
                    # Caso leitura de string
                    while (char != '"' and char is not None):
                        #le toda a cadeia 
                        lexem = lexem + char
                        char = self.getChar()
                    #retorna o token de cadeia
                    return token.Token(self.type.CADEIA,lexem,self.line)