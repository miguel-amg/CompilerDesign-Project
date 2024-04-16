# ----------------------------------------------------
# Projeto final Processamento de Linguagens
# Leonardo Filipe Lima Barroso, a100894
# Miguel Ângelo Martins Guimarães, a100837
# Pedro Andrade Carneiro, a100652
# ----------------------------------------------------

# Uso do programa:
# Ir inserindo as expressões manualmente e clicando enter.
# Assim que estiverem todas inseridas fazer CTRL + D (Visual studio)
#
# Alternativamente poderá ser inserido um ficheiro atráves do comando:
# python3 anaSin.py < testFile.txt 

#################################### GRAMATICA ####################################
#  start -> cont                    // P1 - Conteudo
#        | COLON ID cont SEMICOLON  // P2 - Função
#
#  cont -> NUM cont         // P3  - Inserir num na stack 
#       | PONTO cont        // P4  - Print 
#       | MAIS cont         // P5  - Soma +
#       | MENOS cont        // P6  - Subtração -
#       | MUL cont          // P7  - Multiplicação *
#       | DIV cont          // P8  - Divisão /
#       | MOD cont          // P9  - Resto da divisã inteira (mod)
#       | DUP cont          // P10 - Duplicar valor na stack
#       | CHAR LETRA cont   // P11 - Inserir letra na stack (TALVEZ TENHA QUE METER NA STRING STACK????????????????????????)
#       | SWAP cont         // P12 - Da swap aos dois ultimos elems 
#       | DROP cont         // P13 - Retira o primeiro elem da stack
#       | STRPRINT cont     // P14 - Dá print a uma string
#       | STRPRINT2 cont    // P15 - Dá print a uma string mas remove espaços consecutivos
#       | COMMENT cont      // P16 - Comentario
#       | ENDCOMMENT cont   // P16 - Comentario de linha
#       | ID cont           // P17 - Chamar função
#       | Empty             // P17 - Vazio

#################################### SETUP ####################################
# Imports
from anaLex import tokens
import ply.yacc as yacc
import sys
import os

# Variáveis hardcoded
localResultado = "result"  # Pasta para os resultados
ficheiroFuncoes   = "recursos/funcoes.txt"  # Ficheiro com a definição das funções para a vm
debug = False # Modo debug ligado ou desligado
funcs = {} # Armazenar o codigo das funções

#################################### BOAS-VINDAS ####################################
print(
"""-------------------------------------
Processamento de Linguagens
Engenharia Informática (3º ano)
Compilador de Forth
-------------------------------------""")

#################################### FUNÇÕES AUXILIARES ####################################
# Guardar o resultaod final obtido
def guardarResultado(local, resultado):
    try:
        # Verificar se existe a pasta
        if not os.path.exists(local): os.makedirs(local)
        
        # Caminho completo para o ficheiro result.txt
        ficheiro = os.path.join(local, "result.txt")

        # Abre o arquivo em modo de escrita
        f = open(ficheiro, "w")
        f.write(resultado)

    except Exception as e:
        raise Exception("Erro ao guardar o resultado: {e}")

# Carregar as funções para injetar no resultado final
def carregarFuncoes(ficheiro):
    try:
        f = open(ficheiro, 'r')
        conteudo = f.read()
        return conteudo
    except FileNotFoundError:
        raise Exception("Ficheiro de funções não encontrado!")
    except Exception as e:
        raise Exception(f"Erro ao carregar funções: {e}")
    
    
####################################  CODIGO  ####################################
#------------------------------- REGRAS PARA START -------------------------------
def p_start_cont(p):
    'start : cont'
    p[0] = p[1]
    if(debug): print("P_start_cont")

# Quando uma função é definida o seu codigo é armazenado para quando for chamada ser inserido diretamente
def p_start_func(p):
    'start : COLON ID cont SEMICOLON'
    p[0] = ''

    global funcs

    # Lançar erro caso já esteja definida esta função
    if(p[2] in funcs):
        raise Exception(f"Compiling; Duplicate function!")
    
    # Armazenar o codigo da função
    funcs[p[2]] = '// Inserida função ' + p[2] + '\n' + p[3] + "// Fim função " + p[2] # Armazenar o codigo da função
    if(debug): print("P_start_cont, Função guardada")
    
#------------------------------- REGRAS PARA CONT ------------------------------- 
def p_cont_num(p):
    'cont : NUM cont'
    p[0] = "PUSHI " + str(p[1]) + '\n' + str(p[2])
    if(debug): print("P_cont_num")

def p_cont_ponto(p):
    'cont : PONTO cont'
    p[0] = "WRITEI\n" + str(p[2])
    if(debug): print("P_cont_ponto")

def p_cont_sum(p):
    'cont : MAIS cont'
    p[0] = "ADD\n" + str(p[2])
    if(debug): print("P_cont_sum ADD")

def p_cont_sub(p):
    'cont : MENOS cont'
    p[0] = "SUB\n" + str(p[2])
    if(debug): print("P_cont_sub SUB")

def p_cont_mul(p):
    'cont : MUL cont'
    p[0] = "MUL\n" + str(p[2])
    if(debug): print("P_cont_mul MUL")

def p_cont_div(p):
    'cont : DIV cont'
    p[0] = "DIV\n" + str(p[2])
    if(debug): print("P_cont_div DIV")

def p_cont_mod(p):
    'cont : MOD cont'
    p[0] = "MOD\n" + str(p[2])
    if(debug): print("P_cont_mod MOD")

def p_cont_dup(p):
    'cont : DUP cont'
    p[0] = "DUP 1\n" + str(p[2]) # Dup 1 na vm é duplicar o primeiro elem
    if(debug): print("P_cont_dup")

def p_cont_letra(p):
    'cont : CHAR LETRA cont'
    p[0] = "PUSHI " + str(ord(p[2])) + '\n' + str(p[3]) # A letra tem de ser int na stack
    if(debug): print("P_cont_letra")

def p_cont_swap(p):
    'cont : SWAP cont'
    p[0] = "SWAP\n" + str(p[2]) 
    if(debug): print("P_cont_swap")

def p_cont_drop(p):
    'cont : DROP cont'
    p[0] = "POP 1\n" + str(p[2]) # Pop 1 na vm tira o primeiro elem da stack 
    if(debug): print("P_cont_drop")

def p_cont_strprint(p):
    'cont : STRPRINT cont' 
    p[0] = f"PUSHS \"{p[1]}\" \nWRITES\n" + str(p[2])  
    if(debug): print("P_cont_strprint")

def p_cont_strprint2(p):
    'cont : STRPRINT2 cont' 
    p[0] = f"PUSHS \"{p[1]}\" \nWRITES\n" + str(p[2]) 
    if(debug): print("P_cont_strprint2")

def p_cont_comment(p):
    'cont : COMMENT cont' 
    p[0] = '' + str(p[2])
    if(debug): print("P_cont_comment")

def p_cont_endcomment(p):
    'cont : ENDCOMMENT cont' 
    p[0] = '' 
    if(debug): print("P_cont_endcomment")

def p_cont_func(p):
    'cont : ID cont' 
    global funcs
    p[0] = funcs[p[1]] 
    if(debug): print("P_cont_func")

def p_cont_empty(p):
    'cont : empty'
    p[0] = ''
    if(debug): print("P_cont_empty")

#------------------------------- REGRAS PARA EMPTY -------------------------------
def p_empty(p):
    'empty :'
    pass
    if(debug): print("P_empty")

#------------------------------- ERROS -------------------------------
def p_error(p):
    print("Erro sintático no input!")
    if p:
        print(f"Erro sintático na posição {p.lexpos}: token '{p.value}'")
    else:
        print("Erro sintático: fim inesperado do input")

#################################### PARSER ####################################
# Construir o parser
parser = yacc.yacc()

# Carregar as funções para inserir no final
funcoes = carregarFuncoes(ficheiroFuncoes)

# Iterar cada linha do input
final = "start\n"
for linha in sys.stdin:
    if(debug): print("DEBUG:")
    result = parser.parse(linha)
    print()
    print("EXPRESSÃO RECEBIDA:")
    print(linha)
    print()
    final += result
final += "stop\n"
# (CODIGO ANTIGO FUNCOES PREDEFINIDAS) final += "stop\n" + funcoes # Colocar no final do resultado as funções e stop 

# Obter resultado final e trata-lo
print("RESULTADO FINAL:")
print(final)
guardarResultado(localResultado, final)
print("Resultado armazenado com sucesso em: " + localResultado + "/resultado.txt")