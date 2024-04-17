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
#       | MAIS cont         // P5  - Soma 
#       | MENOS cont        // P6  - Subtração 
#       | MUL cont          // P7  - Multiplicação 
#       | DIV cont          // P8  - Divisão 
#       | MOD cont          // P9  - Resto da divisã inteira
#       | DUP cont          // P10 - Duplicar valor na stack
#       | CHAR LETRA cont   // P11 - Inserir letra na stack (TALVEZ TENHA QUE METER NA STRING STACK????????????????????????)
#       | SWAP cont         // P12 - Da swap aos dois ultimos elems 
#       | DROP cont         // P13 - Retira o primeiro elem da stack
#       | STRPRINT cont     // P14 - Dá print a uma string
#       | STRPRINT2 cont    // P15 - Dá print a uma string mas remove espaços consecutivos
#       | COMMENT cont      // P16 - Comentario
#       | ENDCOMMENT cont   // P17 - Comentario de linha
#       | ID cont           // P18 - Chamar função
#       | NIP cont          // P19 - Remove o segundo item da stack
#       | 2DROP cont        // P20 - Remove os dois elementos no topo da stack
#       | ROT cont          // P21 - Coloca o terceiro item no topo
#       | OVER cont         // P22 - Faz uma copia do segundo item e coloca no topo
#       | 2DUP cont         // P20 - Duplica o par no topo da stack 
#       | 2SWAP cont        // P20 - Troca os dois pares no topo da stack 
#       | 2OVER cont        // P21 - Copiar o 2o par no topo da stack e colar no topo da stack
#       | Empty             // P23 - Vazio

#################################### SETUP ####################################
# Imports
from anaLex import tokens
import ply.yacc as yacc
import sys
import os

# Variáveis hardcoded
localResultado = "result"              # Pasta para os resultados
ficheiroStart  = "recursos/start.txt"  # Ficheiro com o inicio do codigo
debug = False                          # Modo debug ligado ou desligado
funcs = {}                             # Armazenar o codigo das funções

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

# Carrega o conteudo de um ficheiro
def carregarTxt(ficheiro):
    try:
        f = open(ficheiro, 'r')
        conteudo = f.read()
        return conteudo
    except FileNotFoundError:
        raise Exception(f'Ficheiro {ficheiro} não encontrado!')
    except Exception as e:
        raise Exception(f"Erro ao carregar {ficheiro}: {e}")
    
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
    
    # Comentarios para identificar as funções
    startComment = '// Função ' + p[2] + '\n'
    endComment   = "// Fim função " + p[2] + "\n"

    # Armazenar o codigo da função
    funcs[p[2]] = startComment + p[3] + endComment # Armazenar o codigo da função
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
    p[0] = funcs[p[1]] + str(p[2])
    if(debug): print("P_cont_func")

def p_cont_nip(p):
    'cont : NIP cont' 
    p[0] = "SWAP\nPOP 1\n" + str(p[2]) 
    if(debug): print("P_cont_nip")

def p_cont_2drop(p):
    'cont : 2DROP cont' 
    p[0] = "POP 2\n" + str(p[2]) 
    if(debug): print("P_cont_2drop")

# Explicação: Guardar os 3 valores no topo da stack na stack temporaria, inserir denovo trocado 
# Resultado: O 3 item foi para o topo
def p_cont_rot(p):
    'cont : ROT cont'
    vmCode = "STOREG 2 \nSTOREG 1 \nSTOREG 0 \nPUSHG 2 \nPUSHG 1 \nPUSHG 0 \n"
    p[0] = vmCode + str(p[2]) 
    if(debug): print("P_cont_rot")

# Explicação: Armazenar o valor no topo, duplicar o 2 valor, inserir denovo o topo, trocar
# Resultado: Foi duplicado o 2 valor do topo da stack e inserido no topo  
def p_cont_over(p):
    'cont : OVER cont'
    vmCode = "STOREG 0 \nDUP 1 \nPUSHG 0 \nSWAP \n"
    p[0] = vmCode + str(p[2]) 
    if(debug): print("P_cont_over")

# Explicação: Duplicar o elemento no topo e armazenar, duplicar o 2 elemento e armazenar, inserir os pares por ordem
# Resultado: O par no topo da stack foi duplicado
def p_cont_2dup(p):
    'cont : 2DUP cont' 
    vmCode = "DUP 1 \nSTOREG 0 \nSTOREG 1 \nDUP 1 \nSTOREG 2 \nSTOREG 3 \nPUSHG 2 \nPUSHG 0 \nPUSHG 3 \nPUSHG 1 \n"
    p[0] = vmCode + str(p[2]) 
    if(debug): print("P_cont_2dup")

# Explicação: Armazenar os dois pares no topo da stack mas inserir com estes trocados, inserir de volta stack  
# Resultado: O 2 pares no topo da stack foram trocados
def p_cont_2swap(p):
    'cont : 2SWAP cont' 
    vmCode = "STOREG 1 \nSTOREG 0 \nSTOREG 3 \nSTOREG 2 \nPUSHG 0 \nPUSHG 1 \nPUSHG 2 \nPUSHG 3 \n"
    p[0] = vmCode + str(p[2]) 
    if(debug): print("P_cont_2swap")

# Explicação: Armazenar os dois pares, duplicar os valores do 2 par, inserir tudo devolta na stack  
# Resultado: O 2o par foi copiado e inserido no topo da stack
def p_cont_2over(p):
    'cont : 2OVER cont' 
    vmCode = "STOREG 1 \nSTOREG 0 \ndup 1 \nSTOREG 3 \nSTOREG 5 \ndup 1 \nSTOREG 2 \nSTOREG 4 \nPUSHG 2 \nPUSHG 3 \nPUSHG 0 \nPUSHG 1 \nPUSHG 4 \nPUSHG 5 \n"
    p[0] = vmCode + str(p[2]) 
    if(debug): print("P_cont_2over")

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

# Iterar cada linha do input
final = carregarTxt(ficheiroStart) + "start\n"
for linha in sys.stdin:
    if(debug): print("DEBUG:")
    result = parser.parse(linha)
    print()
    print("EXPRESSÃO RECEBIDA:")
    print(linha)
    print()
    final += result
final += "stop\n"

# Obter resultado final e trata-lo
print("RESULTADO FINAL:")
print(final)
guardarResultado(localResultado, final)
print("Resultado armazenado com sucesso em: " + localResultado + "/resultado.txt")