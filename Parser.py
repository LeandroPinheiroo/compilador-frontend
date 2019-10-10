import Scanner as scanner
import Type as T
import Token as token
class Parser:

    def __init__(self):
        self.t = T.Type()
        self.scanner = None
        self.current_token = None

    def interpreter(self, nomeArquivo):
        if not self.scanner is None:
            print('ERRO: Já existe um arquivo sendo processado.')
        else:
            self.scanner = scanner.Scanner(nomeArquivo)
            self.scanner.open_file()
            self.current_token = self.scanner.getToken()

            self.PROG()
            self.consume_token( self.t.FIMARQ )

            self.scanner.close_file() 
    
    def current_equal_previous(self, token):
        #(const, msg) = token
        return self.current_token.type == token

    def consume_token(self, type):
        print(self.current_token.type)
        if self.current_equal_previous( type ):
            self.current_token = self.scanner.getToken()
        else:
            (const, msg) = type
            print('ERRO DE SINTAXE [linha %d]: era esperado "%s" mas veio "%s"'
               % (self.current_token.line, msg, self.current_token.lexem))
            quit()

    def PROG(self):
        self.consume_token(self.t.PROGRAMA)
        self.consume_token(self.t.ID)
        self.consume_token(self.t.PVIRG)
        self.DECLS()
        self.C_COMP()

    def DECLS(self):
        if self.current_equal_previous(self.t.VARIAVEIS):
            self.consume_token(self.t.VARIAVEIS)
            self.LIST_DECLS()
    
    def LIST_DECLS(self):
        self.DECL_TIPO()
        self.D()
    
    def D(self):
        if self.current_equal_previous(self.t.FIMARQ):
            pass
        else:
            self.LIST_DECLS()
    
    def DECL_TIPO(self):
        self.LIST_ID()
        self.consume_token(self.t.DPONTOS)
        self.TIPO()
        self.consume_token(self.t.PVIRG)

    def LIST_ID(self):
        self.consume_token(self.t.ID)
        self.E()
    
    def E(self):
        if self.current_equal_previous(self.t.VIRG):
            self.consume_token(self.t.VIRG)
            self.LIST_ID()
    
    def TIPO(self):
        if self.current_equal_previous(self.t.INTEIRO):
            self.consume_token(self.t.INTEIRO)
        elif self.current_equal_previous(self.t.REAL):
            self.consume_token(self.t.REAL)
        elif self.current_equal_previous(self.t.LOGICO):
            self.consume_token(self.t.LOGICO)
        elif self.current_equal_previous(self.t.CARACTER):
            self.consume_token(self.t.CARACTER)
    
    def C_COMP(self):
        self.consume_token(self.t.ABRECH)
        self.LISTA_COMANDOS()
        self.consume_token(self.t.FECHACH)
    
    def LISTA_COMANDOS(self):
        self.COMANDOS()
        self.G()
    
    def COMANDOS(self):
        if self.current_equal_previous(self.t.SE):
            self.IF()
        elif self.current_equal_previous(self.t.ENQUANTO):
            self.WHILE()
        elif self.current_equal_previous(self.t.LEIA):
            self.READ()
        elif self.current_equal_previous(self.t.ESCREVA):
            self.WRITE()
        elif self.current_equal_previous(self.t.ATRIB):
            self.ATRIB()
    
    def G(self):
        if self.current_equal_previous(self.t.FIMARQ):
            pass
        else:
            self.LISTA_COMANDOS()
    
    def IF(self):
        self.consume_token(self.t.ABREPAR)
        self.EXPR()
        self.consume_token(self.t.FECHAPAR)
        self.C_COMP()
        self.H()

    def H(self):
        if self.current_equal_previous(self.t.SENAO):
            self.consume_token(self.t.SENAO)
            self.C_COMP
    
    def WHILE(self):
        self.consume_token(self.t.ENQUANTO)
        self.consume_token(self.t.ABREPAR)
        self.EXPR()
        self.consume_token(self.t.FECHAPAR)
        self.C_COMP()

    def READ(self):
        self.consume_token(self.t.LEIA)
        self.consume_token(self.t.ABREPAR)
        self.LIST_ID()
        self.consume_token(self.t.FECHAPAR)
        self.consume_token(self.t.PVIRG)
    
    def ATRIB(self):
        self.consume_token(self.t.ID)
        self.consume_token(self.t.ATRIB)
        self.EXPR()
        self.consume_token(self.t.PVIRG)

    def WRITE(self):
        self.consume_token(self.t.ESCREVA)
        self.consume_token(self.t.ABREPAR)
        self.LIST_W()
        self.consume_token(self.t.FECHAPAR)
        self.consume_token(self.t.PVIRG)
    
    def LIST_W(self):
        self.ELEM_W()
        self.L()

    def L():
        if self.current_equal_previous(self.t.VIRG):
            self.consume_token(self.t.VIRG)
            self.LIST_W()
    
    def ELEM_W(self):
        if self.current_equal_previous(self.t.CADEIA):
            self.consume_token(self.t.CADEIA)
        else:
            self.EXPR()
    
    def EXPR(self):
        self.SIMPLES()
        self.P()
    
    def P(self):
        if self.current_equal_previous(self.t.OPREL):
            self.consume_token(self.t.OPREL)
            self.SIMPLES()
    
    def SIMPLES(self):
        self.TERMO
        self.R

    def R(self):
        if self.current_equal_previous(self.t.OPAD):
            self.consume_token(self.t.OPAD)
            self.SIMPLES()
    
    def TERMO(self):
        self.FAT()
        self.F()
    
    def S():
        if self.current_equal_previous(self.t.OPMUL):
            self.consume_token(self.t.OPMUL)
            self.TERMO()

    def FAT(self):
        if self.current_equal_previous(self.t.ID):
            self.consume_token(self.t.ID)
        elif self.current_equal_previous(self.t.CTE):
            self.consume_token(self.t.CTE)
        elif self.current_equal_previous(self.t.ABREPAR):
            self.consume_token(self.t.ABREPAR)
            self.EXPR()
            self.consume_token(self.t.FECHAPAR)
        elif self.current_equal_previous(self.t.VERDADEIRO):
            self.consume_token(self.t.VERDADEIRO)
        elif self.current_equal_previous(self.t.FALSO):
            self.consume_token(self.t.FALSO)
        elif self.current_equal_previous(self.t.OPNEG):
            self.consume_token(self.t.OPNEG)
            self.FAT()