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
#  cont -> cont type
#        | ε
#
#  type -> arit      -- operações aritmeticas
#        | comment   -- comentarios
#        | func      -- funções
#        | stack     -- operações de stack
#        | compare   -- operações de comparação
#        | print     -- operações de print
#
#  -------------------------------------------------------------------------------
#
#  arit -> MAIS    -- Soma 
#        | MENOS   -- Subtração 
#        | MUL     -- Multiplicação 
#        | DIV     -- Divisão 
#        | MOD     -- Resto da divisão inteira
#        | ABS     -- Retorna o absoluto do valor no topo da stack.
#
#  comment -> COMMENT     -- Comentario
#           | ENDCOMMENT  -- Comentario de linha
#
#  func -> COLON ID cont SEMICOLON  -- Definir função
#        | ID                       -- Chamar função
#
#  stack -> NUM        -- Inserir num na stack 
#         | CHAR LETRA -- Inserir letra na stack 
#         | KEY        -- Recebe como input um caracter/tecla e coloca no topo da stack.
#         | DROP       -- Retira o primeiro elem da stack
#         | DUP        -- Duplicar valor na stack
#         | SWAP       -- Da swap aos dois ultimos elems 
#         | NIP        -- Remove o segundo item da stack
#         | 2DROP      -- Remove os dois elementos no topo da stack
#         | ROT        -- Coloca o terceiro item no topo
#         | OVER       -- Faz uma copia do segundo item e coloca no topo
#         | 2DUP       -- Duplica o par no topo da stack 
#         | 2SWAP      -- Troca os dois pares no topo da stack 
#         | 2OVER      -- Copiar o 2o par no topo da stack e colar no topo da stack
#         | TUCK       -- Insere uma copia do primeiro elemento debaixo do segundo
#         | NUM PICK   -- Faz uma copia do n-esimo elemento da stack
#
#  compare -> EQ       -- Retorna verdade se os dois valores no topo da stack forem iguais.
#           | NEQ      -- Retorna verdade se os dois valores no topo da stack forem diferentes.
#           | MENOR    -- Retorna verdade se o 2 valor no topo da stack for menor que o primeiro. Infixo: 10 < 2, Posfixo: 10 2 <.
#           | MAIOR    -- Retorna verdade se o 2 valor no topo da stack for maior que o primeiro. Infixo: 10 > 2, Posfixo: 10 2 >.
#           | ZEROEQ   -- Retorna verdade se o valor no topo da stack for igual de zero.
#           | ZERONEQ  -- Retorna verdade se o valor no topo da stack for diferente de zero.
#           | NEGATE   -- Nega o numero no topo da stack.
#           | MIN      -- Retorna o menor dos dois valores no topo da stack.
#           | MAX      -- Retorna o maior dos dois valores no topo da stack.
#
#  print -> PONTO      -- Print do elemento no topo da stack
#         | EMIT       -- Dá print ao caracter na primeira posição da stack, o caracter é representado em ascii. 
#         | STRPRINT   -- Print a uma string
#         | STRPRINT2  -- Print a uma string mas remove espaços consecutivos
#         | NUM SPACES -- Print a uma determinada quantidade de espaços (Exige um numero antes que é verificado por gramatica).
#         | SPACE      -- Print a um espaço.
#         | CR         -- Print a um new-line (\n).
#
#  cond -> IF cont ELSE cont THEN 
#        | IF cont THEN cont 
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
global condCounter       # Contador para o numero de condições

localResultado  = "result"                # Pasta para os resultados
ficheiroStart   = "recursos/start.txt"    # Ficheiro com o inicio do codigo
ficheiroFuncoes = "recursos/funcoes.txt"  # Ficheiro as funções utilizadas na vm
debug = False  # Modo debug ativo ou inativo (Inativo por predefinição)
funcs = {}     # Armazenar o codigo das funções
funcoesProtegidas = set() # Contém os nomes de todas as funções do sistema. Utilizado para impedir repetições.
condCounter = 0 # Contador para o numero de condições

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
# ---------------------------------- CONTEUDO ----------------------------------
# Conteudo regras
def p_cont_op(p):
    'cont : cont type'
    p[0] = p[1] + p[2]
    if(debug): print("P_cont_op")

def p_cont_empty(p):
    'cont : empty'
    p[0] = ''
    if(debug): print("P_cont_empty")

# ---------------------------------- TYPE ----------------------------------
def p_type_arit(p):
    'type : arit'
    p[0] = p[1]
    if(debug): print("P_type_arit")

def p_type_comment(p):
    'type : comment'
    p[0] = p[1]
    if(debug): print("P_type_comment")

def p_type_func(p):
    'type : func'
    p[0] = p[1]
    if(debug): print("P_type_func")

def p_type_stack(p):
    'type : stack'
    p[0] = p[1]
    if(debug): print("P_type_stack")

def p_type_compare(p):
    'type : compare'
    p[0] = p[1]
    if(debug): print("P_type_compare")

def p_type_print(p):
    'type : print'
    p[0] = p[1]
    if(debug): print("P_type_print")
    
def p_type_cond(p):
    'type : cond'
    p[0] = p[1]
    if(debug): print("P_type_cond")
# ----------------------------------------------------------------- ARIT -----------------------------------------------------------------
def p_arit_sum(p):
    'arit : MAIS'
    p[0] = "ADD\n"
    if(debug): print("P_arit_sum")

def p_arit_sub(p):
    'arit : MENOS'
    p[0] = "SUB\n"
    if(debug): print("P_arit_sub")

def p_arit_mul(p):
    'arit : MUL'
    p[0] = "MUL\n"
    if(debug): print("P_arit_mul")

def p_arit_div(p):
    'arit : DIV'
    p[0] = "DIV\n"
    if(debug): print("P_arit_div")

def p_arit_mod(p):
    'arit : MOD'
    p[0] = "MOD\n"
    if(debug): print("P_arit_mod")

# Explicação: Irá utilizar a função definida no ficheiro de funções vmAbs. Remove o valor inicial e deixa so o resultado.
# Resultado: É inserido o absoluto do valor no topo da stack.
def p_arit_abs(p):
    'arit : ABS' 
    p[0] = "// Função ABS (sistema) \nPUSHA vmAbs \nCALL \nSWAP \nPOP 1 \n// Fim Função ABS (sistema) \n"
    if(debug): print("P_arit_abs")

    
# ----------------------------------------------------------------- COMMENT ----------------------------------------------------------------- 
def p_comment_one(p):
    'comment : COMMENT' 
    p[0] = ''
    if(debug): print("P_comment_one")

def p_op_endcomment(p):
    'comment : ENDCOMMENT' 
    p[0] = '' 
    if(debug): print("P_comment_endcomment")

# ----------------------------------------------------------------- FUNC -----------------------------------------------------------------
# Quando uma função é definida o seu codigo é armazenado para quando for chamada ser inserido diretamente
def p_func_define(p):
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
    if(debug): print("P_func_define, Função guardada")
    
def p_func_call(p):
    'func : ID' 
    global funcs

    print(str(funcs))

    # Verificar se a função foi definida antes de ser chamada
    if p[1] in funcs:
        p[0] = funcs[p[1]]
    else:
        # Se não estiver definida, gere uma mensagem de erro
        raise Exception(f"Erro de compilacao, identificador de função desconhecido \"{p[1]}\".")
    
    if(debug): print("P_func_call")
    
# ----------------------------------------------------------------- STACK ----------------------------------------------------------------- 
# DESATIVADO (Funcionamento incorreto)
#def p_cont_pick(p):
#    'cont : NUM PICK cont'
#    p[0] = "PUSHL " + str(p[1]) + '\n' + str(p[3]) 
#    if(debug): print("P_cont_pick")

def p_stack_num(p):
    'stack : NUM'
    p[0] = "PUSHI " + str(p[1]) + '\n'
    if(debug): print("P_stack_num")

def p_stack_dup(p):
    'stack : DUP'
    p[0] = "DUP 1\n" # Dup 1 na vm é duplicar o primeiro elem
    if(debug): print("P_stack_dup")

def p_stack_letra(p):
    'stack : CHAR LETRA'
    p[0] = "PUSHI " + str(ord(p[2])) + '\n' # A letra tem de ser int na stack
    if(debug): print("P_stack_letra")

def p_stack_swap(p):
    'stack : SWAP'
    p[0] = "SWAP\n"
    if(debug): print("P_stack_swap")

def p_stack_drop(p):
    'stack : DROP'
    p[0] = "POP 1\n" # Pop 1 na vm tira o primeiro elem da stack 
    if(debug): print("P_stack_drop")

def p_stack_nip(p):
    'stack : NIP' 
    p[0] = "SWAP\nPOP 1\n"
    if(debug): print("P_stack_nip")

def p_stack_2drop(p):
    'stack : 2DROP' 
    p[0] = "POP 2\n"
    if(debug): print("P_stack_2drop")

# Explicação: Guardar os 3 valores no topo da stack na stack temporaria, inserir denovo trocado 
# Resultado: O 3 item foi para o topo
def p_stack_rot(p):
    'stack : ROT'
    vmCode = "STOREG 2 \nSTOREG 1 \nSTOREG 0 \nPUSHG 2 \nPUSHG 1 \nPUSHG 0 \n"
    p[0] = vmCode
    if(debug): print("P_stack_rot")

# Explicação: Armazenar o valor no topo, duplicar o 2 valor, inserir denovo o topo, trocar
# Resultado: Foi duplicado o 2 valor do topo da stack e inserido no topo  
def p_stack_over(p):
    'stack : OVER'
    vmCode = "STOREG 0 \nDUP 1 \nPUSHG 0 \nSWAP \n"
    p[0] = vmCode
    if(debug): print("P_stack_over")

# Explicação: Duplicar o elemento no topo e armazenar, duplicar o 2 elemento e armazenar, inserir os pares por ordem
# Resultado: O par no topo da stack foi duplicado
def p_stack_2dup(p):
    'stack : 2DUP' 
    vmCode = "DUP 1 \nSTOREG 0 \nSTOREG 1 \nDUP 1 \nSTOREG 2 \nSTOREG 3 \nPUSHG 2 \nPUSHG 0 \nPUSHG 3 \nPUSHG 1 \n"
    p[0] = vmCode
    if(debug): print("P_stack_2dup")

# Explicação: Armazenar os dois pares no topo da stack mas inserir com estes trocados, inserir de volta stack  
# Resultado: O 2 pares no topo da stack foram trocados
def p_stack_2swap(p):
    'stack : 2SWAP' 
    vmCode = "STOREG 1 \nSTOREG 0 \nSTOREG 3 \nSTOREG 2 \nPUSHG 0 \nPUSHG 1 \nPUSHG 2 \nPUSHG 3 \n"
    p[0] = vmCode
    if(debug): print("P_stack_2swap")

# Explicação: Armazenar os dois pares, duplicar os valores do 2 par, inserir tudo devolta na stack  
# Resultado: O 2o par foi copiado e inserido no topo da stack
def p_stack_2over(p):
    'stack : 2OVER' 
    vmCode = "STOREG 1 \nSTOREG 0 \ndup 1 \nSTOREG 3 \nSTOREG 5 \ndup 1 \nSTOREG 2 \nSTOREG 4 \nPUSHG 2 \nPUSHG 3 \nPUSHG 0 \nPUSHG 1 \nPUSHG 4 \nPUSHG 5 \n"
    p[0] = vmCode 
    if(debug): print("P_stack_2over")

def p_stack_tuck(p):
    'stack : TUCK' 
    vmCode = "DUP 1 \nSTOREG 0 \nSTOREG 2 \nSTOREG 1 \nPUSHG 0 \nPUSHG 1 \nPUSHG 2 \n"
    p[0] = vmCode
    if(debug): print("P_stack_tuck")

# ----------------------------------------------------------------- COMPARE -----------------------------------------------------------------
def p_compare_eq(p):
    'compare : EQ' 
    p[0] = "EQUAL \n"
    if(debug): print("P_compare_eq")

def p_compare_neq(p):
    'compare : NEQ' 
    p[0] = "EQUAL \nPUSHI 0 \nEQUAL \n"
    if(debug): print("P_compare_neq")

def p_compare_menor(p):
    'compare : MENOR' 
    p[0] = "INF \n"
    if(debug): print("P_compare_menor")

def p_compare_maior(p):
    'compare : MAIOR' 
    p[0] = "SUP \n"
    if(debug): print("P_compare_maior")

def p_compare_zeroeq(p):
    'compare : ZEROEQ' 
    p[0] = "NOT \n"
    if(debug): print("P_compare_zeroeq")

def p_compare_zeromaior(p):
    'compare : ZEROMAIOR' 
    p[0] = "PUSHI 0 \nSUP \n"
    if(debug): print("P_compare_zeromaior")

def p_compare_zeromenor(p):
    'compare : ZEROMENOR' 
    p[0] = "PUSHI 0 \nINF \n"
    if(debug): print("P_compare_zeromenor")

def p_compare_zeroneq(p):
    'compare : ZERONEQ' 
    p[0] = "NOT \nPUSHI 0 \nEQUAL \n"
    if(debug): print("P_compare_zeroneq")

def p_compare_negate(p):
    'compare : NEGATE' 
    p[0] = "PUSHI -1 \nMUL \n"
    if(debug): print("P_compare_negate")

# Explicação: Irá utilizar a função definida no ficheiro de funções vmMin. Remove os 2 valores iniciais e deixa so o resultado.
# Resultado: É inserido o menor valor de entre os 2 no topo da stack.
def p_compare_min(p):
    'compare : MIN' 
    p[0] = "// Função MIN (sistema) \nPUSHA vmMin \nCALL  \nSWAP \nPOP 1 \nSWAP \nPOP 1 \n// Fim Função MIN (sistema) \n" 
    if(debug): print("P_compare_min")

# Explicação: Irá utilizar a função definida no ficheiro de funções vmMax. Remove os 2 valores iniciais e deixa so o resultado.
# Resultado: É inserido o maior valor de entre os 2 no topo da stack.
def p_compare_max(p):
    'compare : MAX' 
    p[0] = "// Função MAX (sistema) \nPUSHA vmMax \nCALL  \nSWAP \nPOP 1 \nSWAP \nPOP 1 \n// Fim Função MAX (sistema) \n"
    if(debug): print("P_compare_max")

# ----------------------------------------------------------------- PRINT -----------------------------------------------------------------
def p_print_strprint(p):
    'print : STRPRINT' 
    p[0] = f"PUSHS \"{p[1]}\" \nWRITES \n"
    if(debug): print("P_print_strprint")

def p_print_strprint2(p):
    'print : STRPRINT2' 
    p[0] = f"PUSHS \"{p[1]}\" \nWRITES \n"
    if(debug): print("P_print_strprint2")

def p_print_ponto(p):
    'print : PONTO'
    p[0] = "WRITEI\n"
    if(debug): print("P_print_ponto")

def p_print_space(p):
    'print : SPACE' 
    p[0] = "PUSHS \" \" \nWRITES \n" + str(p[2]) 
    if(debug): print("P_print_space")

def p_print_cr(p):
    'print : CR' 
    p[0] = "WRITELN \n"
    if(debug): print("P_print_cr")

# Função utilizada esta definida no ficheiro funcoes.txt
def p_print_spaces(p):
    'print : SPACES'
    p[0] = f"STOREG 0 \nPUSHA spaceloop \nCALL\n" 
    if(debug): print("P_print_spaces")

# CUIDADO: Esta implementação do emit não irá transformar o int no caracter correspondente, 
# , já que não é possivel realizar esta conversão na EWVM, 
# , foi ponderada a criação de um função com uma grande quantidade de ifs para realizar a conversão.
def p_print_emit(p):
    'print : EMIT' 
    vmCode = "STRI \nWRITES \n"
    p[0] = vmCode
    if(debug): print("P_print_emit")

# ----------------------------------------------------------------- CONDS -----------------------------------------------------------------
def p_cond_iet(p):
    'cond : IF cont ELSE cont THEN' 
    
    # Contador para o numero de condicionais
    global condCounter
    id = str(condCounter) 

    # Criação do nome das labels
    labelIf = "if" + id; labelElse = "else" + id; labelThen = "then" + id

    # Criação do codigo
    chamada = f"PUSHA {labelIf} \nCALL \n"                                                                                          
    conteudoIF = f"{labelIf}: \nPUSHFP \nLOAD -1 \nJZ {labelElse} \n{p[2]}JUMP {labelThen} \n"  
    conteudoELSE = f"{labelElse}: \n{p[4]}JUMP {labelThen}\n" 
    conteudoTHEN = f"{labelThen}: \n"

    # Comentarios
    startComment = f"//------ Condicional {id} ------ \n"
    endComment   = f"//------------------------------ \n"

    p[0] = startComment + chamada + '\n' + conteudoIF + '\n' + conteudoELSE + '\n' + conteudoTHEN + '\n' + endComment 
    
    if(debug): print("P_cond_iet")

def p_cond_it(p):
    'cond : IF cont THEN' 
    
    # Contador para o numero de condicionais
    global condCounter
    id = str(condCounter) 

    # Criação do nome das labels
    labelIf = "if" + id; labelThen = "then" + id

    # Criação do codigo
    chamada = f"PUSHA {labelIf} \nCALL \n"                                                                                          
    conteudoIF = f"{labelIf}: \nPUSHFP \nLOAD -1 \nJUMP {labelThen} \n"  
    conteudoTHEN = f"{labelThen}: \n"

    # Comentarios
    startComment = f"//------ Condicional {id} ------ \n"
    endComment   = f"//------------------------------ \n"

    p[0] = startComment + chamada + '\n' + conteudoIF + '\n' + conteudoTHEN + '\n' + endComment 
    
    if(debug): print("P_cond_it")

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
if(not debug): final = carregarTxt(ficheiroStart) + "\nstart\n" + result + "stop\n\n" + carregarTxt(ficheiroFuncoes)
if(debug): final = result # Em modo debug apenas é apresentado o conteudo do result

# Obter resultado final e trata-lo
print()
print("RESULTADO FINAL:")
print(final)
guardarResultado(localResultado, final)
print("Resultado armazenado com sucesso em: " + localResultado + "/resultado.txt")