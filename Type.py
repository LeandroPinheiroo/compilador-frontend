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
    OPREL = (18,'oprel')
    # operadores aritméticos
    OPAD = (19, 'opad')
    OPMUL = (20, 'opmul')
    # restantes dos operadores
    OPNEG = (21, '!')
    PVIRG = (22, ';')
    DPONTOS = (23, ':')
    VIRG = (24, ',')
    ABREPAR = (25, '(')
    FECHAPAR = (26, ')')
    ABRECH = (27, '{')
    FECHACH = (28, '}')
    ERRO = (666, 'ERRO')
    FIMARQ = (29, 'endfile')