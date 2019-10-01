class Type:
    def __init__(self):
        pass
    # tokens relacionados ao programa
    ID = (1, 'id')
    CTE = (2, 'num')
    CADEIA = (3, 'cadeia')
    PROGRAMA = (4, 'programa')
    VARIAVEIS = (5, 'variaveis')
    # tokens relacionados a tipo de dados
    INTEIRO = (6, 'inteiro')
    REAL = (7, 'real')
    LOGICO = (8, 'logico')
    CARACTER = (9, 'caracter')
    # tokens relacionados a comandos da linguagem
    SE = (10, 'se')
    SENAO = (11, 'senao')
    ENQUANTO = (12, 'enquanto')
    LEIA = (13, 'leia')
    ESCREVA = (14, 'escreva')
    FALSO = (15, 'falso')
    VERDADEIRO = (16, 'verdadeiro')
    ATRIB = (17, ':=')
    # operadores relacionais
    IGUAL = (18, '=')
    MENORQ = (19, '<')
    MAIORQ = (20, '>')
    MENORIQ = (21, '<=')
    MAIORIG = (22, '>=')
    DIF = (23, '<>')
    # operadores aritméticos
    ADI = (24, '+')
    SUB = (25, '-')
    DIV = (26, '/')
    MULT = (27, '*')
    # restantes dos operadores
    OPNEG = (28, '!')
    PVIRG = (29, ';')
    DPONTOS = (30, ':')
    VIRG = (31, ',')
    ABREPAR = (32, '(')
    FECHAPAR = (33, ')')
    ABRECH = (34, '{')
    FECHACH = (35, '}')
    ERRO = (666, 'ERRO')
    FIMARQ = (36, 'endfile')