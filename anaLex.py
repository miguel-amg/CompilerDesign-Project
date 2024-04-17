# ----------------------------------------------------
# Projeto final Processamento de Linguagens
# Leonardo Filipe Lima Barroso, a100894
# Miguel Ângelo Martins Guimarães, a100837
# Pedro Andrade Carneiro, a100652
# ----------------------------------------------------

###########################
# PARA RESOLVER
# O : NAO PODE ESTAR COLADO A NADA
# + NAO PODE TAR COLADO A NADA
# tem de funcionar dar multilinha as funções 
###########################



# Imports
import ply.lex as lex
import re

######################## FUNÇÕES AUXILIARES ########################
# Transforma espaços continuos em um so espaço
def removeEspacos(string):
    regex = r'\s+'
    return re.sub(regex, " ", string)

######################## TOKENS ########################
# Tokens reservados
reserved = {
   'MOD'  : 'MOD',   # mod  | resto da divisao inteira 
   'EMIT' : 'EMIT',  # emit | dá print a um char (passa de int para char)
   'CHAR' : 'CHAR',  # char | declarar um caracter
   'DUP'  : 'DUP',   # dup  | duplicar valor na stack
   'SWAP' : 'SWAP',  # swap | trocar os dois ultimos valores na stack
   'DROP' : 'DROP',  # drop | retira o primeiro elem da stack
   'OVER' : 'OVER',  # over | faz uma copia do segundo item e coloca no topo
   'ROT'  : 'ROT',   # rot  | coloca o terceiro item no topo
   'NIP'  : 'NIP'    # nip  | remove o segundo item da stack
}

# Todos os tokens
tokens = (
    "MAIS",       # +                    | Adição
    "MENOS",      # -                    | Subtração
    "MUL",        # *                    | Multiplicação
    "DIV",        # /                    | Divisão
    "PONTO",      # .                    | Print do valor no topo da stack
    "COLON",      # :                    | Inicio de uma função
    "SEMICOLON",  # ;                    | Fim de função
    "2DROP",      # 2DROP                | Remove os dois elementos no topo da stack
    "2DUP",       # 2DUP                 | Duplicar o par no topo da stack
    "2SWAP",      # 2SWAP                | Troca os dois pares no topo da stack
    "2OVER",      # 2OVER                | Copiar o 2o par apartir do topo da stack e cola no topo da mesma
    "NUM",        # 123                  | Numero
    "ID",         # abc123               | Usado nas funções como nome
    "STRPRINT",   # ." txttxtxtxt txtxt" | Realiza print ao texto entre aspas
    "STRPRINT2",  # .( txttxtxtxt txtxt) | Realiza print ao texto entre parentesis e transforma espaços consecutivos em um só espaço
    "COMMENT",    # ( txtxt txtxt)       | É um comentario
    "ENDCOMMENT", # \ txtxtx             | É um comentario de linha
    "LETRA"       # A                    | Representa uma letra
    # TALVEZ ADICIONAR .( TXTXTX MOSTRAR DURANTE COMPILAÇÃO)
) + tuple(reserved.values())

######################## REGEX ########################
# Tokens
t_MAIS = r'\+'
t_MENOS = r"- " # Colado do lado esquerdo tem significado de negativo nos numeros
t_MUL = r'\*'
t_DIV = r'/'
t_PONTO = r'^\. |\s\.\s| \.$' # Print do valor no topo da stack (O ponto nunca esta colado a nada) (talvez com tab morra?)
t_COLON = r':'                # Inicio de função 
t_SEMICOLON = r';'            # Fim de função
t_COMMENT = r'\(\s[^\)]+\)'   # Comentario
t_ENDCOMMENT = r'\\.+'        # Comentario de linha
t_LETRA = r'[A-Za-z]'         # Regex para reconhecer uma única letra

# Colocado como função para ser verificado primeiro que o id e num
# Remover 2 elementos do topo da stack
def t_2DROP(t):
    r'(?i)2DROP'
    return t

# Colocado como função para ser verificado primeiro que o id e num
# Duplicar o par no topo da stack
def t_2DUP(t):
    r'(?i)2DUP'  
    return t

# Colocado como função para ser verificado primeiro que o id e num
# Trocar os dois pares no topo da stack
def t_2SWAP(t):
    r'(?i)2SWAP' 
    return t

# Colocado como função para ser verificado primeiro que o id e num
# Copiar o 2o par apartir do topo da stack e cola no topo da mesma
def t_2OVER(t):
    r'(?i)2OVER' 
    return t

def t_NUM(t):
    r"(\+|-)?\d+"
    t.value = int(t.value)
    return t

# Nome de função
def t_ID(t):
    r'[A-Za-z_][A-Za-z_0-9]+'
    t.type = reserved.get(t.value.upper(),'ID') # Verificar se leu uma palavra reservada sem querer, senão valor default = VAR
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
    print(f"TOKEN não reconhecido: {t.value[0]}")
    t.lexer.skip(1)

######################## FIM ########################
lexer = lex.lex()