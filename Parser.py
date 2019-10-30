########################################################################
# João Paulo de Souza    - 0035329                                     #
# Leandro Souza Pinheiro - 0015137                                     #
# Trabalho Compiladores  - Front-end do compilador para a linguagem P  #
# Data: 31/10/2019                                                     #
########################################################################

import Scanner as scanner
import Type as T
import Token as token
import SymbolsTable as st
class Parser:
    #construtor da classe parser, responsavel por declarar o tipo do token e iniciar o scanner e token atual
    def __init__(self):
        self.t = T.Type()
        self.scanner = None
        self.current_token = None
        self.symbols_table = st.SymbolsTable()

    #metodo principal da classe, onde iniciara a leitura do arquivo e irá instanciar o scanner
    def interpreter(self, nomeArquivo):
        if not self.scanner is None: #caso o scanner ja tenha sido instanciado
            print('ERRO: Já existe um arquivo sendo processado.')#mostra erro
        else:#caso contrario 
            #instacia o scanner
            self.scanner = scanner.Scanner(nomeArquivo)
            #abre arquivo a ser compilado
            self.scanner.open_file()
            #pega o primeiro token
            self.current_token = self.scanner.getToken()
            #chama metodo inicial
            self.A()
            #fecha o arquivo compilado corretamente
            self.scanner.close_file() 
    
    #metodo responsavel por realizar a comparacao entre o token atual e o token que era esperado
    def current_equal_previous(self, token):
        #(const, msg) = token
        #realiza comparacao e retorna TRUE ou FALSE
        return self.current_token.type == token

    #metodo responsavel por realizar o consumo do token atual
    def consume_token(self, type):
        #print(self.current_token.type)
        #verifica se o token atual é igual ao token esperado
        if self.current_equal_previous( type ):
            #se sim pede o novo token
            self.current_token = self.scanner.getToken()
            if (self.current_token.type == self.t.ID):
                self.symbols_table.insert(self.current_token.lexem, self.current_token.type, None, None, self.current_token.line)
        else:#caso contrario mostra mensagem de erro na linha em questao
            (const, msg) = type
            print('ERRO DE SINTAXE [linha %d]: era esperado "%s" mas veio "%s"'
               % (self.current_token.line, msg, self.current_token.lexem))
            #nextToken = self.scanner.getToken()
            #while(not (nextToken.type == self.t.FECHACH or nextToken.type == self.t.PVIRG)):
            #    if nextToken.type == self.t.FIMARQ:
            #        quit()
            #    nextToken = self.scanner.getToken()?
            self.current_token = self.scanner.getToken()
            # quit() #mata o programa

    #metodo inicial resposavel por receber o programa e depois obrigatoriamente o fim de arquivo 
    def A(self):
        self.PROG()
        #obrigatoriamente no final é necessário consumir o token de fim de arquivo
        self.consume_token( self.t.FIMARQ )

    #metodo inicial de producoes da gramatica, responsavel por ler a declaracao do programa 
    def PROG(self):
        #consome tokens 
        self.consume_token(self.t.PROGRAMA)
        self.consume_token(self.t.ID)
        self.consume_token(self.t.PVIRG)
        #chama metodo para declaracao de variaveis
        self.DECLS()
        #metodo responsavel por realizar a abertura/fechamento de chaves e receber uma lista de comando
        self.C_COMP()

    #metodo responsavel por realizar declaracao de variaveis
    def DECLS(self):
        #se o token atual e uma variavel
        if self.current_equal_previous(self.t.VARIAVEIS):
            #realiza o consumo do token
            self.consume_token(self.t.VARIAVEIS)
            #chama funcao para receber novas declaracoes caso possua
            self.LIST_DECLS()
        else:#caso contrario terminou de ler as declaracoes,ou seja foi recebido lambda na producao da gramatica
            pass
    
    #metodo responsavel por realizar uma lista de declaracoes
    def LIST_DECLS(self):
        #recebe o tipo de declaracao
        self.DECL_TIPO()
        #metodo para realizar novas leituras ou terminar a leitura de declaracoes
        self.D()

    #metodo para realizar novas leituras ou terminar a leitura de declaracoes
    def D(self):
        #se leu fim de arquivo ou entao nao leu um token do tipo ID
        if self.current_equal_previous(self.t.FIMARQ) or not self.current_equal_previous(self.t.ID):
            pass #terminou as declaracoes e apenas passa
        else:#se nao ainda precisa declarar variaveis
            self.LIST_DECLS() #chama funcao responsavel
    
    #metodo responsavel por realizar as declaracoes de variaveis
    #Nele eh chamado os metodos responsaveis por realizar a declaracao 
    def DECL_TIPO(self):
        self.LIST_ID()
        self.consume_token(self.t.DPONTOS)
        self.TIPO()
        self.consume_token(self.t.PVIRG)
    #Metodo responsavel por receber um ID e chamar metodo para ler novas variaveis
    def LIST_ID(self):
        self.consume_token(self.t.ID)
        self.E()
    #metood responsavel por receber novas variaveis de mesmo tipo separadas por virgula
    def E(self):
        #caso tenha virgula indica que tera novas variaveis declaradas
        if self.current_equal_previous(self.t.VIRG):
            self.consume_token(self.t.VIRG)
            self.LIST_ID()#chama metodo para ler novo ID
        else:#caso contrario apenas passa
            pass
    #metoodo responsavel por receber o tipo de cada varivel
    def TIPO(self):
        #tipos validos (INTEIRO, REAL, LOGICO e CARACTER)
        if self.current_equal_previous(self.t.INTEIRO):
            self.consume_token(self.t.INTEIRO)
        elif self.current_equal_previous(self.t.REAL):
            self.consume_token(self.t.REAL)
        elif self.current_equal_previous(self.t.LOGICO):
            self.consume_token(self.t.LOGICO)
        elif self.current_equal_previous(self.t.CARACTER):
            self.consume_token(self.t.CARACTER)
    
    #Metodo responsavel por receber uma lista de comandos entre chaves
    #Exemplo: Utilizado ao encontrar um SE, que tem um bloco de comandos ente {}
    def C_COMP(self):
        self.consume_token(self.t.ABRECH)
        self.LISTA_COMANDOS()
        self.consume_token(self.t.FECHACH)
    
    #Metodo responsavel por receber uma lista de comandos
    def LISTA_COMANDOS(self):
        self.COMANDOS() #le o comando necessario
        self.G() 
    #metodo responsavel por receber um comando 
    #comandos validos sao SE, ENQUANTO, LEIA, ESCREVE e algum ID
    def COMANDOS(self):
        if self.current_equal_previous(self.t.SE):
            self.IF()
        elif self.current_equal_previous(self.t.ENQUANTO):
            self.WHILE()
        elif self.current_equal_previous(self.t.LEIA):
            self.READ()
        elif self.current_equal_previous(self.t.ESCREVA):
            self.WRITE()
        elif self.current_equal_previous(self.t.ID):
            self.ATRIB()
        else:#caso nao seja nenhum comando valido apenas passa por indicar ser um producao para vazio
            pass
    #metodo responsavel por realizar as novas leituras de comandos 
    def G(self):
        if not self.current_equal_previous(self.t.SE) and not self.current_equal_previous(self.t.ENQUANTO) and not self.current_equal_previous(self.t.LEIA) and not self.current_equal_previous(self.t.ESCREVA) and not self.current_equal_previous(self.t.ID):
            pass #caso proximo token nao for um comando, apenas passa para frente
        elif self.current_equal_previous(self.t.FIMARQ): #caso encontre o fim de arquivo apenas passa
            pass
        else:# se nao indica que sera necessario receber uma nova lista de comandos
            self.LISTA_COMANDOS()
    
    #metodo responsavel por receber um comando do tipo IF
    def IF(self):
        #consome os tokens que representam o IF
        self.consume_token(self.t.SE)
        self.consume_token(self.t.ABREPAR)
        self.EXPR() #expressao do if
        self.consume_token(self.t.FECHAPAR)
        self.C_COMP()# bloco de computacoes
        self.H()#metodo que ira identificar se existe um SENAO

    #Metodo responsavel por verificar se apos p comando IF existe um SENAO
    def H(self):
        if self.current_equal_previous(self.t.SENAO): #verifica se o token eh um SENAO
            self.consume_token(self.t.SENAO) #consome o token
            self.C_COMP() #metodo para receber o bloco de computacoes
        else:
            pass
    #Metodo responsavel por receber um laco de repeticao do TIPO WHILE
    def WHILE(self):
        #consome tokens para montar o while
        self.consume_token(self.t.ENQUANTO)
        self.consume_token(self.t.ABREPAR)
        self.EXPR() #metodo para receber a expressao
        self.consume_token(self.t.FECHAPAR)
        self.C_COMP() #metodo para receber o bloco de computacoes que ira repetir

    #metodo responsavel por receber um comando do tipo LEITURA
    def READ(self):
        #consome os tokens para montar a leitura
        self.consume_token(self.t.LEIA)
        self.consume_token(self.t.ABREPAR)
        self.LIST_ID() # metodo para receber a lista de id
        #tokens que finalizam a leitura
        self.consume_token(self.t.FECHAPAR)
        self.consume_token(self.t.PVIRG)
    
    #metoodo responsavel por receber um comando do tipo atribuicao 
    def ATRIB(self):
        #consome os tokens para iniciar a atribuicao a um ID 
        self.consume_token(self.t.ID)
        self.consume_token(self.t.ATRIB)
        self.EXPR() #recebe a expresao
        self.consume_token(self.t.PVIRG) #ao final recebe um ponto e virgula
    
    #metodo responsavel por receber um comando do tipo ESCRITA
    def WRITE(self):
        #consome os tokens para iniciar a escrita
        self.consume_token(self.t.ESCREVA)
        self.consume_token(self.t.ABREPAR)
        self.LIST_W() #monta a lista que sera escrita
        #recebe os tokens para finalizar a escrita
        self.consume_token(self.t.FECHAPAR)
        self.consume_token(self.t.PVIRG)
    
    # Metodo responsavel por iniciar o recebimento do que sera escrito
    def LIST_W(self):
        self.ELEM_W() #metodo para verificar se sera escrito atualmente uma cadeia ou uma expressao
        self.L() # chama metodo responsavel por verificar se existe uma concatenacao dentro da escrita

    #metodo responsavel por verificar se existe uma concatenacao dentro da escrita
    def L(self):
        if self.current_equal_previous(self.t.VIRG): #caso encontre a virgula existe a concatenacao
            self.consume_token(self.t.VIRG) #consome a virgula 
            self.LIST_W() #chama metodo e repete
        else:#caso contrario apenas passa para frente
            pass
    #metodo responsavel por identificar se o que sera escrito eh uma cadeia ou uma expressao
    def ELEM_W(self):
        if self.current_equal_previous(self.t.CADEIA):
            self.consume_token(self.t.CADEIA)
        else:
            self.EXPR()
    #metodo responsavel por receber uma expressao
    def EXPR(self):
        self.SIMPLES()
        self.P()
    #metodo resposnavel por receber uma expressao relacional
    def P(self):
        if self.current_equal_previous(self.t.OPREL):
            self.consume_token(self.t.OPREL)
            self.SIMPLES()
        else:
            pass
    #metodo responsavel por receber expressoes simples
    def SIMPLES(self):
        self.TERMO()
        self.R()
    #metodo responsavel por receber expressoes de adicao e subtracao
    def R(self):
        #caso leia o token de adicao e subtracao
        if self.current_equal_previous(self.t.OPAD):
            #consome e repete a leitura da expressao
            self.consume_token(self.t.OPAD)
            self.SIMPLES()
        else:#apenas passa
            pass
    #metodo responsavel por receber um termo
    def TERMO(self):
        self.FAT()
        self.S()
    #metodo responsavel por receber um operador de multiplicacao
    def S(self):
        #caso token MUL
        if self.current_equal_previous(self.t.OPMUL):
            self.consume_token(self.t.OPMUL)
            self.TERMO()
        else:#caso contrario apenas passa
            pass
    #metodo responsavel por receber um fator
    def FAT(self):
        #os fatores validos sao:
        if self.current_equal_previous(self.t.ID): # ID
            self.consume_token(self.t.ID)
        elif self.current_equal_previous(self.t.CTE): # CTE(NUMERO)
            self.consume_token(self.t.CTE)
        elif self.current_equal_previous(self.t.ABREPAR): # ABREPARENTESE(obrigatorio fehchar)
            self.consume_token(self.t.ABREPAR)
            self.EXPR()
            self.consume_token(self.t.FECHAPAR)
        elif self.current_equal_previous(self.t.VERDADEIRO): # VERDADEIRO
            self.consume_token(self.t.VERDADEIRO)
        elif self.current_equal_previous(self.t.FALSO): # FALSO
            self.consume_token(self.t.FALSO)
        elif self.current_equal_previous(self.t.OPNEG): # NEGACAO DE UM NOVO FATOR
            self.consume_token(self.t.OPNEG)
            self.FAT()
        else:#caso contrario apenas passa
            pass
