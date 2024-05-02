# ----------------------------------------------------
# Projeto final Processamento de Linguagens
# Leonardo Filipe Lima Barroso, a100894
# Miguel Ângelo Martins Guimarães, a100837
# Pedro Andrade Carneiro, a100652
# ----------------------------------------------------

# Imports
import ply.lex as lex
import re

######################## FUNÇÕES AUXILIARES ########################
# Transforma espaços continuos em um so espaço
def removeEspacos(string):
    regex = r'\s+'
    return re.sub(regex, " ", string)

######################## TOKENS ########################
# Tokens reservados (Utilizado pelo ID para evitar conflitos)
reserved = {
   'MOD'    : 'MOD',    # mod    | Resto da divisao inteira .
   'EMIT'   : 'EMIT',   # emit   | Dá print ao caracter na primeira posição da stack, o caracter é representado em ascii. 
   'DUP'    : 'DUP',    # dup    | Duplicar valor na stack.
   'SWAP'   : 'SWAP',   # swap   | Trocar os dois ultimos valores na stack.
   'DROP'   : 'DROP',   # drop   | Retira o primeiro elem da stack.
   'OVER'   : 'OVER',   # over   | Faz uma copia do segundo item e coloca no topo.
   'ROT'    : 'ROT',    # rot    | Coloca o terceiro item no topo.
   'NIP'    : 'NIP',    # nip    | Remove o segundo item da stack.
   'TUCK'   : 'TUCK',   # tuck   | Insere uma copia do primeiro elemento debaixo do segundo.
   #'PICK'   : 'PICK',  # pick   | Faz uma copia do n-esimo elemento da stack (Exige um numero antes que é verificado por gramatica).
   'KEY'    : 'KEY',    # key    | Input de um caracter/tecla.
   'SPACE'  : 'SPACE',  # space  | Dá output a um espaço.
   'SPACES' : 'SPACES', # spaces | Dá output a uma determinada quantidade de espaços (Exige um numero antes que é verificado por gramatica).
   'CR'     : 'CR',     # cr     | Dá output a um new-line (\n).
   'NEGATE' : 'NEGATE', # negate | Nega o numero no topo da stack.
   'MIN'    : 'MIN',    # min    | Retorna o menor dos dois valores no topo da stack.
   'MAX'    : 'MAX',    # max    | Retorna o maior dos dois valores no topo da stack.
   'ABS'    : 'ABS',    # abs    | Retorna o absoluto do valor no topo da stack.
   'IF'     : 'IF',     # if     | Inicio de um bloco if.
   'ELSE'   : 'ELSE',   # else   | Fim de um bloco if.
   'THEN'   : 'THEN',   # then   | Fim de um bloco if.
   'DEPTH'  : 'DEPTH',  # depth  | Retorna o numero de elementos na stack.
   'DO'     : 'DO',     # do     | Inicio de um loop.
   'LOOP'   : 'LOOP',   # loop   | Fim de um loop.
   'I'      : 'I',      # i      | Valor do contador do loop.
}

# Todos os tokens
tokens = (
    "MAIS",       # +                    | Adição.
    "MENOS",      # -                    | Subtração.
    "MUL",        # *                    | Multiplicação.
    "DIV",        # /                    | Divisão.
    "PONTO",      # .                    | Print do valor no topo da stack.
    "COLON",      # :                    | Inicio de uma função.
    "SEMICOLON",  # ;                    | Fim de função.
    "2DROP",      # 2DROP                | Remove os dois elementos no topo da stack.
    "2DUP",       # 2DUP                 | Duplicar o par no topo da stack.
    "2SWAP",      # 2SWAP                | Troca os dois pares no topo da stack.
    "2OVER",      # 2OVER                | Copiar o 2o par apartir do topo da stack e cola no topo da mesma.
    "NUM",        # 123                  | Numero.
    "ID",         # abc123               | Usado nas funções como nome.
    "STRPRINT",   # ." txttxtxtxt txtxt" | Realiza print ao texto entre aspas.
    "STRPRINT2",  # .( txttxtxtxt txtxt) | Realiza print ao texto entre parentesis e transforma espaços consecutivos em um só espaço.
    "COMMENT",    # ( txtxt txtxt)       | É um comentario.
    "ENDCOMMENT", # \ txtxtx             | É um comentario de linha.
    "ZEROEQ",     # 0=                   | Retorna verdade se o valor no topo da stack for igual a zero.
    "ZERONEQ",    # 0<>                  | Retorna verdade se o valor no topo da stack for diferente de zero.
    "ZEROMENOR",  # 0<                   | Retorna verdade se o valor no topo da stack for menor que zero.
    "ZEROMAIOR",  # 0>                   | Retorna verdade se o valor no topo da stack for maior que zero.
    "EQ",         # =                    | Retorna verdade se os dois valores no topo da stack forem iguais.
    "NEQ",        # <>                   | Retorna verdade se os dois valores no topo da stack forem diferentes.
    "MENOR",      # <                    | Retorna verdade se o 2 valor no topo da stack for menor que o primeiro. Nota: (Infixo: 10 < 2, Posfixo: 10 2 <).
    "MAIOR",      # >                    | Retorna verdade se o 2 valor no topo da stack for maior que o primeiro. Nota: (Infixo: 10 > 2, Posfixo: 10 2 >).
    "MENOREQ",    # <=                   | Retorna verdade se o 2 valor no topo da stack for menor ou igual ao primeiro. Nota: (Infixo: 10 <= 2, Posfixo: 10 2 <=).
    "MAIOREQ",    # >=                   | Retorna verdade se o 2 valor no topo da stack for maior ou igual ao primeiro. Nota: (Infixo: 10 >= 2, Posfixo: 10 2 >=).
    "1SUM",       # 1+                   | Adiciona 1 ao valor no topo da stack.
    "1SUB",       # 1-                   | Subtrai 1 ao valor no topo da stack.
    "2DIV",       # 2/                   | Divide o valor no topo da stack por 2.
    "CHARLETRA"   # char c               | Le um char seguido de uma letra.
    # ADICIONAR .( TXTXTX MOSTRAR DURANTE COMPILAÇÃO)
    # ADICIONAR /MOD
) + tuple(reserved.values())

######################## REGEX ########################
# NOTA: Formula para forçar TXT a estar separado de outros tokens: (?<!\S)TXT(?!\S)  
t_MAIS  = r'(?<!\S)\+(?!\S)'
t_MENOS = r'(?<!\S)-(?!\S)'  # O - nao pode estar colado a nada para ter o significado de sub
t_MUL   = r'(?<!\S)\*(?!\S)'
t_DIV   = r'(?<!\S)/(?!\S)'
t_PONTO = r'(?<!\S)\.(?!\S)'  # Print do valor no topo da stack (O ponto nunca esta colado a nada) (talvez com tab morra?)
t_COLON = r'(?<!\S)\:(?!\S)'  # Inicio de função 
t_SEMICOLON  = r'(?<!\S);(?!\S)'             # Fim de função
t_COMMENT    = r'(?<!\S)\(\s[^\)]+\)(?!\S)'  # Comentario
t_ENDCOMMENT = r'\\.+'                       # Comentario de linha
t_ZEROEQ     = r'(?<!\S)0=(?!\S)'
t_ZERONEQ    = r'(?<!\S)0<>(?!\S)'
t_ZEROMENOR  = r'(?<!\S)0<(?!\S)'
t_ZEROMAIOR  = r'(?<!\S)0>(?!\S)'
t_EQ    = r'(?<!\S)=(?!\S)'
t_NEQ   = r'(?<!\S)<>(?!\S)'
t_MENOR = r'(?<!\S)<(?!\S)'
t_MAIOR = r'(?<!\S)>(?!\S)'
t_MENOREQ = r'(?<!\S)<=(?!\S)'
t_MAIOREQ = r'(?<!\S)>=(?!\S)'
t_2OVER = r'(?<!\S)(?i)2OVER(?!\S)'
t_2SWAP = r'(?<!\S)(?i)2SWAP(?!\S)'
t_2DUP  = r'(?<!\S)(?i)2DUP(?!\S)'
t_2DROP = r'(?<!\S)(?i)2DROP(?!\S)'
t_1SUM  = r'(?<!\S)1\+(?!\S)'
t_1SUB  = r'(?<!\S)1-(?!\S)'
t_2DIV  = r'(?<!\S)2/(?!\S)'

def t_CHARLETRA(t):
    r'(?<!\S)char\s[A-Za-z](?!\S)'
    t.value = t.value[5:] # O valor é a letra
    return t

# Regra para os numeros
def t_NUM(t):
    r"(?<!\S)(\+|-)?\d+(?!\S)"
    t.value = int(t.value)
    return t

# Nome de função
def t_ID(t):
    r'(?<!\S)[A-Za-z_][A-Za-z_0-9]*(?!\S)'
    t.type = reserved.get(t.value.upper(),'ID') # Verificar se leu uma palavra reservada sem querer, senão valor default = ID
    return t

# Dá print a uma string | ." txtxtxtx txtxtx"
def t_STRPRINT(t):
    r'\."\s[^"]+"'
    t.value = t.value[3:-1]  # O valor é o conteudo da string entre aspas
    return t

# Dá print a uma string | .(txtxtxtx     txtxtx) | transforma espaços consequetivos em um só
def t_STRPRINT2(t):
    r'\.\(\s[^\)]+\)'
    conteudoStr = t.value[3:-1]  # O valor é o conteudo da string entre parentesis
    t.value = removeEspacos(conteudoStr)
    return t

t_ignore = ' \n\t\r'

def t_error(t):
    print(f"AnaLex: Token desconhecido {t.value[0]}")
    t.lexer.skip(1)

######################## FIM ########################
lexer = lex.lex()