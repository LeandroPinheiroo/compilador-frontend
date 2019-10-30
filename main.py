import Scanner as scanner
import Type as type
import Parser as parser
import sys as s


if __name__ == "__main__":
    """
    scaninho = scanner.Scanner('exemplo1.txt')
    scaninho.open_file()
    token = scaninho.getToken()
    while(token.type != type.Type().FIMARQ):
        print(str(token.type) , " -> " , str(token.line))
        token = scaninho.getToken()
    """
    arg = s.argv
    parser = parser.Parser()
    parser.interpreter('./2019923_233811_compiladores1-trabalho1-2019-2/testes-trabalho-1-2019-2/exemplo1.txt')
    if (len(arg) == 2):
        if (arg[1] == '-p'):
            parser.symbols_table.printTable()
        else:
            print('Comando inválido')
    elif (len(arg) == 3):
        if (arg[1] == '-t'):
            fileName = arg[2]
            parser.symbols_table.exportToFile(fileName)
        else:
            print('Comando inválido')