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
#  cont -> NUM cont
#       | PONTO cont  
#       | op cont
#       | Empty
#
#  op -> + | - | / | *

#################################### SETUP ####################################
# Imports
from anaLex import tokens
import ply.yacc as yacc
import sys

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

####################################  CODIGO  ####################################
#------------------------------- REGRAS PARA CONT ------------------------------- 
def p_cont_num(p):
    'cont : NUM cont'
    p[0] = "PUSHI " + str(p[1]) + '\n' + str(p[2])
    if(debug): print("P_cont_num")

def p_cont_ponto(p):
    'cont : PONTO cont'
    p[0] = "WRITEI\n" + str(p[2])
    if(debug): print("P_cont_ponto ")

def p_cont_op(p):
    'cont : op cont'
    p[0] = p[1] + p[2]
    if(debug): print("P_cont_op")

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