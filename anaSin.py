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
#
# Pode-se entrar no modo debug iniciando o programa com:
# python3 anaSin.py debug

#################################### GRAMATICA ####################################
#  exp -> exp func 
#       | exp cont
#       | empty
# 
#  func -> COLON ID cont SEMICOLON
#
#  cont -> cont op
#       | empty
#
#  op ->  NUM SPACES  // P3  - Dá output a uma determinada quantidade de espaços (Exige um numero antes que é verificado por gramatica).
#       | NUM PICK    // P4  - Faz uma copia do n-esimo elemento da stack
#       | NUM         // P5  - Inserir num na stack 
#       | PONTO       // P6  - Print 
#       | MAIS        // P7  - Soma 
#       | MENOS       // P8  - Subtração 
#       | MUL         // P9  - Multiplicação 
#       | DIV         // P10 - Divisão 
#       | MOD         // P11 - Resto da divisã inteira
#       | DUP         // P12 - Duplicar valor na stack
#       | CHAR LETRA  // P13 - Inserir letra na stack 
#       | SWAP        // P14 - Da swap aos dois ultimos elems 
#       | DROP        // P15 - Retira o primeiro elem da stack
#       | STRPRINT    // P16 - Dá print a uma string
#       | STRPRINT2   // P17 - Dá print a uma string mas remove espaços consecutivos
#       | COMMENT     // P18 - Comentario
#       | ENDCOMMENT  // P19 - Comentario de linha
#       | ID          // P20 - Chamar função
#       | NIP         // P21 - Remove o segundo item da stack
#       | 2DROP       // P22 - Remove os dois elementos no topo da stack
#       | ROT         // P23 - Coloca o terceiro item no topo
#       | OVER        // P24 - Faz uma copia do segundo item e coloca no topo
#       | 2DUP        // P25 - Duplica o par no topo da stack 
#       | 2SWAP       // P26 - Troca os dois pares no topo da stack 
#       | 2OVER       // P27 - Copiar o 2o par no topo da stack e colar no topo da stack
#       | TUCK        // P28 - Insere uma copia do primeiro elemento debaixo do segundo
#       | EMIT        // P29 - Dá print ao caracter na primeira posição da stack, o caracter é representado em ascii. 
#       | KEY         // P30 - Recebe como input um caracter/tecla e coloca no topo da stack.
#       | SPACE       // P31 - Da output a um espaço.
#       | CR          // P32 - Dá output a um new-line (\n).
#       | EQ          // P33 - Retorna verdade se os dois valores no topo da stack forem iguais.
#       | NEQ         // P33 - Retorna verdade se os dois valores no topo da stack forem diferentes.
#       | MENOR       // P34 - Retorna verdade se o 2 valor no topo da stack for menor que o primeiro. Infixo: 10 < 2, Posfixo: 10 2 <.
#       | MAIOR       // P35 - Retorna verdade se o 2 valor no topo da stack for maior que o primeiro. Infixo: 10 > 2, Posfixo: 10 2 >.
#       | ZEROEQ      // P36 - Retorna verdade se o valor no topo da stack for igual de zero.
#       | ZERONEQ     // P37 - Retorna verdade se o valor no topo da stack for diferente de zero.
#       | NEGATE      // P38 - Nega o numero no topo da stack.
#       | MIN         // P38 - Retorna o menor dos dois valores no topo da stack.
#       | MAX         // P38 - Retorna o maior dos dois valores no topo da stack.
#       | ABS         // P39 - Retorna o absoluto do valor no topo da stack.
#       | Empty       // P38 - Vazio

#################################### SETUP ####################################
# Imports
from anaLex import tokens
import ply.yacc as yacc
import sys
import os
import re

# Variáveis 
global debug             # (Valor é alterado pela função tratarArgumentos)
global funcoesProtegidas # (Valor é alterado pela função carregarFuncoesProtegidas) 

localResultado  = "result"                # Pasta para os resultados
ficheiroStart   = "recursos/start.txt"    # Ficheiro com o inicio do codigo
ficheiroFuncoes = "recursos/funcoes.txt"  # Ficheiro as funções utilizadas na vm
debug = False  # Modo debug ativo ou inativo (Inativo por predefinição)
funcs = {}     # Armazenar o codigo das funções
funcoesProtegidas = set() # Contém os nomes de todas as funções do sistema. Utilizado para impedir repetições.

#################################### BOAS-VINDAS ####################################
print(
"""-------------------------------------
Processamento de Linguagens
Engenharia Informática (3º ano)
Compilador de Forth
-------------------------------------""")

#################################### FUNÇÕES AUXILIARES ####################################
# Guardar o resultado final obtido
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

# Carrega os nomes de todas as funções do sistema para dentro de um conjunto
def carregarFuncProtegidas(ficheiro):
    funcStart = r'([A-Za-z_][A-Za-z_0-9]+):'
    with open(ficheiro, 'r') as file:
        texto = file.read()
        matches = re.findall(funcStart, texto)
        return set(matches)

# Trata dos argumentos passados para o programa
def tratarArgumentos(argumentos):
    global debug

    # Verificar a quantidade de argumentos recebidos
    if len(argumentos) == 2:
        # Verificar o argumento recebido
        if argumentos[1].lower() == 'debug': debug = True
        else: raise Exception("Programa: Argumento com valor desconhecido!")    
    elif len(argumentos) > 2:
        raise Exception("Programa: Demasiados argumentos!")

####################################  CODIGO  ####################################
# ---------------------------------- EXPRESSAO ----------------------------------

def p_exp_func(p):
    'exp : func exp'
    p[0] = p[1] + p[2]
    if(debug): print("P_exp_func")
    
def p_exp_cont(p):
    'exp : cont exp'
    p[0] = p[1] + p[2]
    if(debug): print("P_exp_cont")

def p_exp_empty(p):
    'exp : empty'
    p[0] = ''
    if(debug): print("P_exp_empty")

# ---------------------------------- CONTEUDO ---------------------------------- 
def p_cont(p):
    'cont : cont op'
    p[0] = p[1] + p[2]
    if(debug): print("P_cont")

def p_cont_empty(p):
    'cont : empty'
    p[0] = ''
    if(debug): print("P_cont_empty")

# ---------------------------------- FUNC ---------------------------------- 
# Quando uma função é definida o seu codigo é armazenado para quando for chamada ser inserido diretamente
def p_func(p):
    'func : COLON ID cont SEMICOLON'

    p[0] = ''
    global funcs, funcoesProtegidas

    # Lançar erro caso já esteja definida esta função
    if(p[2] in funcs):
        raise Exception(f"Erro de compilacao, funcao \"{p[2]}\" duplicada!")
    
    # Impedir que o utilizador use função com nome de função do sistema
    if(p[2] in funcoesProtegidas): 
        raise Exception(f"Erro de compilacao, nome \"{p[2]}\" utilizado por funcao do sistema! \nFunções utilizadas pelo sistema: {funcoesProtegidas}")

    # Comentarios para identificar as funções
    startComment = '// Função ' + p[2] + '\n'
    endComment   = "// Fim função " + p[2] + "\n"

    # Armazenar o codigo da função
    funcs[p[2]] = startComment + p[3] + endComment # Armazenar o codigo da função
    if(debug): print("P_cont_def_func, Função guardada")
    

# ---------------------------------- OP ----------------------------------
def p_op_spaces(p):
    'op : NUM SPACES'
    spaces_str = ""
    for n in range(int(p[1])): spaces_str += " "  # Criar uma string com o numero de espaços pretendidos 
    p[0] = f"PUSHS \"{spaces_str}\" \nWRITES \n" 
    if(debug): print("P_op_spaces")

# DESATIVADO (Funcionamento incorreto)
#def p_cont_pick(p):
#    'cont : NUM PICK cont'
#    p[0] = "PUSHL " + str(p[1]) + '\n' + str(p[3]) 
#    if(debug): print("P_cont_pick")

def p_op_num(p):
    'op : NUM'
    p[0] = "PUSHI " + str(p[1]) + '\n'
    if(debug): print("P_op_num")

def p_op_ponto(p):
    'op : PONTO'
    p[0] = "WRITEI\n"
    if(debug): print("P_op_ponto")

def p_op_sum(p):
    'op : MAIS'
    p[0] = "ADD\n"
    if(debug): print("P_op_sum ADD")

def p_op_sub(p):
    'op : MENOS'
    p[0] = "SUB\n"
    if(debug): print("P_op_sub SUB")

def p_op_mul(p):
    'op : MUL'
    p[0] = "MUL\n"
    if(debug): print("P_op_mul MUL")

def p_op_div(p):
    'op : DIV'
    p[0] = "DIV\n"
    if(debug): print("P_op_div DIV")

def p_op_mod(p):
    'op : MOD'
    p[0] = "MOD\n"
    if(debug): print("P_op_mod MOD")

def p_op_dup(p):
    'op : DUP'
    p[0] = "DUP 1\n" # Dup 1 na vm é duplicar o primeiro elem
    if(debug): print("P_op_dup")

def p_op_letra(p):
    'op : CHAR LETRA'
    p[0] = "PUSHI " + str(ord(p[2])) + '\n' # A letra tem de ser int na stack
    if(debug): print("P_op_letra")

def p_op_swap(p):
    'op : SWAP'
    p[0] = "SWAP\n"
    if(debug): print("P_op_swap")

def p_op_drop(p):
    'op : DROP'
    p[0] = "POP 1\n" # Pop 1 na vm tira o primeiro elem da stack 
    if(debug): print("P_op_drop")

def p_op_strprint(p):
    'op : STRPRINT' 
    p[0] = f"PUSHS \"{p[1]}\" \nWRITES \n"
    if(debug): print("P_op_strprint")

def p_op_strprint2(p):
    'op : STRPRINT2' 
    p[0] = f"PUSHS \"{p[1]}\" \nWRITES \n"
    if(debug): print("P_op_strprint2")

def p_op_comment(p):
    'op : COMMENT' 
    p[0] = ''
    if(debug): print("P_op_comment")

def p_op_endcomment(p):
    'op : ENDCOMMENT' 
    p[0] = '' 
    if(debug): print("P_op_endcomment")

def p_op_func(p):
    'op : ID' 
    global funcs

    print(str(funcs))

    # Verificar se a função foi definida antes de ser chamada
    if p[1] in funcs:
        p[0] = funcs[p[1]]
    else:
        # Se não estiver definida, gere uma mensagem de erro
        raise Exception(f"Erro de compilacao, identificador de função desconhecido \"{p[1]}\".")
    
    if(debug): print("P_op_func")

def p_op_nip(p):
    'op : NIP' 
    p[0] = "SWAP\nPOP 1\n"
    if(debug): print("P_op_nip")

def p_op_2drop(p):
    'op : 2DROP' 
    p[0] = "POP 2\n"
    if(debug): print("P_op_2drop")

# Explicação: Guardar os 3 valores no topo da stack na stack temporaria, inserir denovo trocado 
# Resultado: O 3 item foi para o topo
def p_op_rot(p):
    'op : ROT'
    vmCode = "STOREG 2 \nSTOREG 1 \nSTOREG 0 \nPUSHG 2 \nPUSHG 1 \nPUSHG 0 \n"
    p[0] = vmCode
    if(debug): print("P_op_rot")

# Explicação: Armazenar o valor no topo, duplicar o 2 valor, inserir denovo o topo, trocar
# Resultado: Foi duplicado o 2 valor do topo da stack e inserido no topo  
def p_op_over(p):
    'op : OVER'
    vmCode = "STOREG 0 \nDUP 1 \nPUSHG 0 \nSWAP \n"
    p[0] = vmCode
    if(debug): print("P_op_over")

# Explicação: Duplicar o elemento no topo e armazenar, duplicar o 2 elemento e armazenar, inserir os pares por ordem
# Resultado: O par no topo da stack foi duplicado
def p_op_2dup(p):
    'op : 2DUP' 
    vmCode = "DUP 1 \nSTOREG 0 \nSTOREG 1 \nDUP 1 \nSTOREG 2 \nSTOREG 3 \nPUSHG 2 \nPUSHG 0 \nPUSHG 3 \nPUSHG 1 \n"
    p[0] = vmCode
    if(debug): print("P_op_2dup")

# Explicação: Armazenar os dois pares no topo da stack mas inserir com estes trocados, inserir de volta stack  
# Resultado: O 2 pares no topo da stack foram trocados
def p_op_2swap(p):
    'op : 2SWAP' 
    vmCode = "STOREG 1 \nSTOREG 0 \nSTOREG 3 \nSTOREG 2 \nPUSHG 0 \nPUSHG 1 \nPUSHG 2 \nPUSHG 3 \n"
    p[0] = vmCode
    if(debug): print("P_op_2swap")

# Explicação: Armazenar os dois pares, duplicar os valores do 2 par, inserir tudo devolta na stack  
# Resultado: O 2o par foi copiado e inserido no topo da stack
def p_op_2over(p):
    'op : 2OVER' 
    vmCode = "STOREG 1 \nSTOREG 0 \ndup 1 \nSTOREG 3 \nSTOREG 5 \ndup 1 \nSTOREG 2 \nSTOREG 4 \nPUSHG 2 \nPUSHG 3 \nPUSHG 0 \nPUSHG 1 \nPUSHG 4 \nPUSHG 5 \n"
    p[0] = vmCode 
    if(debug): print("P_op_2over")

def p_op_tuck(p):
    'op : TUCK' 
    vmCode = "DUP 1 \nSTOREG 0 \nSTOREG 2 \nSTOREG 1 \nPUSHG 0 \nPUSHG 1 \nPUSHG 2 \n"
    p[0] = vmCode
    if(debug): print("P_op_tuck")

# CUIDADO: Esta implementação do emit não irá transformar o int no caracter correspondente, 
# , já que não é possivel realizar esta conversão na EWVM, 
# , foi ponderada a criação de um função com uma grande quantidade de ifs para realizar a conversão.
def p_op_emit(p):
    'op : EMIT' 
    vmCode = "STRI \nWRITES \n"
    p[0] = vmCode
    if(debug): print("P_op_emit")

def p_op_space(p):
    'op : SPACE' 
    p[0] = "PUSHS \" \" \nWRITES \n" + str(p[2]) 
    if(debug): print("P_op_space")

def p_op_cr(p):
    'op : CR' 
    p[0] = "WRITELN \n"
    if(debug): print("P_op_cr")

def p_op_eq(p):
    'op : EQ' 
    p[0] = "EQUAL \n"
    if(debug): print("P_op_eq")

def p_op_neq(p):
    'op : NEQ' 
    p[0] = "EQUAL \nPUSHI 0 \nEQUAL \n"
    if(debug): print("P_op_neq")

def p_op_menor(p):
    'op : MENOR' 
    p[0] = "INF \n"
    if(debug): print("P_op_menor")

def p_op_maior(p):
    'op : MAIOR' 
    p[0] = "SUP \n"
    if(debug): print("P_op_maior")

def p_op_zeroeq(p):
    'op : ZEROEQ' 
    p[0] = "NOT \n"
    if(debug): print("P_op_zeroeq")

def p_op_zeromaior(p):
    'op : ZEROMAIOR' 
    p[0] = "PUSHI 0 \nSUP \n"
    if(debug): print("P_op_zeromaior")

def p_op_zeromenor(p):
    'op : ZEROMENOR' 
    p[0] = "PUSHI 0 \nINF \n"
    if(debug): print("P_op_zeromenor")

def p_op_zeroneq(p):
    'op : ZERONEQ' 
    p[0] = "NOT \nPUSHI 0 \nEQUAL \n"
    if(debug): print("P_op_zeroneq")

def p_op_negate(p):
    'op : NEGATE' 
    p[0] = "PUSHI -1 \nMUL \n"
    if(debug): print("P_op_negate")

# Explicação: Irá utilizar a função definida no ficheiro de funções vmMin. Remove os 2 valores iniciais e deixa so o resultado.
# Resultado: É inserido o menor valor de entre os 2 no topo da stack.
def p_op_min(p):
    'op : MIN' 
    p[0] = "// Função MIN (sistema) \nPUSHA vmMin \nCALL  \nSWAP \nPOP 1 \nSWAP \nPOP 1 \n// Fim Função MIN (sistema) \n" 
    if(debug): print("P_op_min")

# Explicação: Irá utilizar a função definida no ficheiro de funções vmMax. Remove os 2 valores iniciais e deixa so o resultado.
# Resultado: É inserido o maior valor de entre os 2 no topo da stack.
def p_op_max(p):
    'op : MAX' 
    p[0] = "// Função MAX (sistema) \nPUSHA vmMax \nCALL  \nSWAP \nPOP 1 \nSWAP \nPOP 1 \n// Fim Função MAX (sistema) \n"
    if(debug): print("P_op_max")

# Explicação: Irá utilizar a função definida no ficheiro de funções vmAbs. Remove o valor inicial e deixa so o resultado.
# Resultado: É inserido o absoluto do valor no topo da stack.
def p_op_abs(p):
    'op : ABS' 
    p[0] = "// Função ABS (sistema) \nPUSHA vmAbs \nCALL \nSWAP \nPOP 1 \n// Fim Função ABS (sistema) \n"
    if(debug): print("P_op_abs")


#------------------------------- REGRAS PARA EMPTY -------------------------------
def p_empty(p):
    'empty :'
    pass
    if(debug): print("P_empty")

#------------------------------- ERROS -------------------------------
def p_error(p):
    if p:
        raise Exception(f"AnaSin: Erro gramatical na posição {p.lexpos}: token {p.value}, tipo {p.type}")
    else:
        raise Exception("AnaSin: Erro, fim inesperado do input")

#################################### PARSER ####################################
# Obter argumentos do programa e trata-los
argumentos = sys.argv
tratarArgumentos(argumentos)

# Inicio
if(debug): print("MODO DEBUG ATIVO:")

# Proteger o utilizador de criar funçoes com o mesmo nome das do sistema
funcoesProtegidas = carregarFuncProtegidas(ficheiroFuncoes)
if(debug): print("Funcoes protegidas: " + str(funcoesProtegidas)) 
    
# Construir o parser
parser = yacc.yacc()

# Iterar o input
result = parser.parse(sys.stdin.read())
final = carregarTxt(ficheiroStart) + "\nstart\n" + result + "stop\n\n" + carregarTxt(ficheiroFuncoes)

# Obter resultado final e trata-lo
print()
print("RESULTADO FINAL:")
print(final)
guardarResultado(localResultado, final)
print("Resultado armazenado com sucesso em: " + localResultado + "/resultado.txt")