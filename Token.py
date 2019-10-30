########################################################################
# João Paulo de Souza    - 0035329                                     #
# Leandro Souza Pinheiro - 0015137                                     #
# Trabalho Compiladores  - Front-end do compilador para a linguagem P  #
########################################################################

import Type as type

class Token:
    def __init__(self, type, lexem, line):
        self.type = type
        self.lexem = lexem
        self.line = line
     
    