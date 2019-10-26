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