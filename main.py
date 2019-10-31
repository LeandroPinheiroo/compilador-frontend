########################################################################
# João Paulo de Souza    - 0035329                                     #
# Leandro Souza Pinheiro - 0015137                                     #
# Trabalho Compiladores  - Front-end do compilador para a linguagem P  #
# Data: 31/10/2019                                                     #
########################################################################

#Importacoes
import Scanner as scanner
import Type as type
import Parser as parser
import sys as s

#MAIN
if __name__ == "__main__":
    arg = s.argv # recebe os parametros passados por linha de comando
    parser = parser.Parser() #chama o parser
    if (len(arg) == 2): # caso a quantidade de argumentos seja 2 indica que nao precisa printar a tabela de simbolos
        parser.interpreter(arg[1]) # chama metodo para realizar interpretacao do arquivo passado
        #arquivo a ser interpretado se encontra na posicao 1 do vetor de argumentos
    elif (len(arg) == 4): #caso a quantidade de argumentos seja 4 indica que precisa printar a tabela de simbolos no arquivo 
        if (arg[2] == '-t'): # obrigatoriamente na posicao 2 dos argumentos necessariamente deve ser -t
            parser.interpreter(arg[1])# chama metodo para realizar interpretacao do arquivo passado
            #arquivo a ser interpretado se encontra na posicao 1 do vetor de argumentos
            fileName = arg[3] #recebe o arquivo de saida que conterá a tabela de simbolos
            parser.symbols_table.exportToFile(fileName) # chama metodo para exportar a tabela de simbolos para o arquivo desejado
        else:#caso contrario foi passado um comando invalido
            print('Comando inválido')
    else:#caso contrario foi passado uma quantidade e argumentos invalido
        print("Número invalido de argumentos passados na linha de comando")