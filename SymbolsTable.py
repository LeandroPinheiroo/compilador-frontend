import Type as t
# class da tabela de simbolos
class SymbolsTable:
    # inicia a tabela vazia
    symbols_table = None
    class Node():
        def __init__(self, type, scope, extras, line):
            self.type = type
            self.scope = scope
            self.extras = extras
            self.line = line
    # e assim que a classe for instanciada, instancia tambem a tabela
    def __init__(self):
        self.symbols_table = {}
    # abaixo segue os métodos da tabela

    # método para inserir os simbolos na tabela, recebe a key, o tipo, o escopo e se há
    # parametros ou outros atributos extras
    def insert(self, key: str, type, scope, extras: [], line: int):
        # cria um node
        node = self.Node(type, scope, extras, line)
        # e insere ele na tabela utilizando a key
        self.symbols_table[key] = node
    
    # método para remover os simbolos na tabela
    def remove(self, key: str):
        self.symbols_table[key] = None
    
    # metodo para buscar um simbolo na tabela
    def get(self, key: str):
        if key in self.symbols_table:
            node = self.symbols_table[key]
            return (node.type, node.scope, node.extras, node.line)
        return None
    
    # metodo para limpar tabela
    def free(self):
        self.symbols_table = None
        self.symbols_table = {}

    #método para buscar a tabela de simbolos
    def getSymbolsTable(self):
        return self.symbols_table
    
    # método para printar a tabela
    def printTable(self):
        print('\t' + 'Chave' + '\t' + 'Tipo' + '\t' + 'Escopo' + '\t' + 'Extras' + '\t' + 'Linha')
        for i in self.symbols_table:
            node = self.get(i)
            print('\t' + i + '\t' + str(node[0]) + '\t' + str(node[1]) + '\t' + str(node[2]) + '\t' + str(node[3]) + '\n')
    # método para exportar a tabela para um arquivo externo    
    def exportToFile(self, fileName):
        file = open(fileName, 'w')
        file.write('\t' + 'Chave' + '\t' + 'Tipo' + '\t' + 'Escopo' + '\t' + 'Extras' + '\t' + 'Linha' + '\n')
        for i in self.symbols_table:
            node = self.get(i)
            file.write('\t' + i + '\t' + str(node[0]) + '\t' + str(node[1]) + '\t' + str(node[2]) + '\t' + str(node[3]) + '\n')
