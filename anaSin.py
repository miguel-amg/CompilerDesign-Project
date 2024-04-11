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
#       | op cont           // P5  - Operação 
#       | DUP cont          // P6  - Duplicar valor na stack
#       | CHAR LETRA cont   // P7  - Inserir letra na stack (TALVEZ TENHA QUE METER NA STRING STACK????????????????????????)
#       | SWAP cont         // P8  - Da swap aos dois ultimos elems (NAO ESTA A FUNCIONAR NA VM!!!!!!!!!!!!!!)
#       | DROP cont         // P9  - Retira o primeiro elem da stack
#       | STRPRINT cont     // P10 - Dá print a uma string
#       | STRPRINT2 cont    // P11 - Dá print a uma string mas remove espaços consecutivos
#       | Empty             // P12 - Vazio
#
#  op -> +      // P13 - Soma
#     | -       // P14 - Subtração
#     | /       // P15 - Divisão
#     | *       // P16 - Multiplicação
#     | mod     // P17 - Resto da divisão inteira
#################################### SETUP ####################################
# Imports
from anaLex import tokens
import ply.yacc as yacc
import sys
import re

# Variáveis hardcoded
localResultado = "result"  # Pasta para os resultados
debug = False               # Modo debug ligado ou desligado

#################################### BOAS-VINDAS ####################################
print(
"""-------------------------------------
Processamento de Linguagens
Engenharia Informática (3º ano)
Compilador de Forth
-------------------------------------""")

#################################### FUNÇÕES AUXILIARES ####################################
def guardarResultado(local, resultado):
    ficheiro = local + "/result.txt"
    f = open(ficheiro, "w")
    f.write(resultado)
    f.close()

# Transforma espaços continuos em um so espaço
def removeEspacos(string):
    regex = r'\s+'
    return re.sub(regex, " ", string)
    

####################################  CODIGO  ####################################
#------------------------------- REGRAS PARA START -------------------------------
def p_start_cont(p):
    'start : cont'
    p[0] = p[1]
    if(debug): print("P_start_cont")

def p_start_func(p):
    'start : COLON ID cont SEMICOLON'
    p[0] = p[1]
    if(debug): print("P_start_cont")
    
#------------------------------- REGRAS PARA CONT ------------------------------- 
def p_cont_num(p):
    'cont : NUM cont'
    p[0] = "PUSHI " + str(p[1]) + '\n' + str(p[2])
    if(debug): print("P_cont_num")

def p_cont_ponto(p):
    'cont : PONTO cont'
    p[0] = "WRITEI\n" + str(p[2])
    if(debug): print("P_cont_ponto")

def p_cont_op(p):
    'cont : op cont'
    p[0] = p[1] + p[2]
    if(debug): print("P_cont_op")

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
    conteudoStr = '\"' + p[1][3:] # O p[1] é igual a ." teste" por isso temos de remover o .
    p[0] = "PUSHS " + conteudoStr + "\nWRITES\n" + str(p[2])  
    if(debug): print("P_cont_strprint")

def p_cont_strprint2(p):
    'cont : STRPRINT2 cont' 
    conteudoStr = '\"' + removeEspacos(p[1][3:-1]) + '\"' # O p[1] é igual a ." teste" por isso temos de remover o .
    p[0] = "PUSHS " + conteudoStr + "\nWRITES\n" + str(p[2]) 
    if(debug): print("P_cont_strprint")

def p_cont_empty(p):
    'cont : empty'
    p[0] = ''
    if(debug): print("P_cont_empty")

#------------------------------- REGRAS PARA OP  -------------------------------
def p_op_sum(p):
    'op : MAIS'
    p[0] = "ADD\n"
    if(debug): print("P_cont_add ADD")

def p_op_menos(p):
    'op : MENOS'
    p[0] = "SUB\n"
    if(debug): print("P_cont_sub SUB")

def p_op_mul(p):
    'op : MUL'
    p[0] = "MUL\n"
    if(debug): print("P_cont_mul MUL")

def p_op_div(p):
    'op : DIV'
    p[0] = "DIV\n"
    if(debug): print("P_cont_div DIV")

def p_op_mod(p):
    'op : MOD'
    p[0] = "MOD\n"
    if(debug): print("P_cont_mod MOD")
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

# Iterar cada linha do input
final = ""
for linha in sys.stdin:
    if(debug): print("DEBUG:")
    result = parser.parse(linha)
    print()
    print("EXPRESSÃO RECEBIDA:")
    print(linha)
    print()
    final += result

# Obter resultado final e trata-lo
print("RESULTADO FINAL:")
print(final)
guardarResultado(localResultado, final)
print("Resultado armazenado com sucesso em: " + localResultado + "/resultado.txt")