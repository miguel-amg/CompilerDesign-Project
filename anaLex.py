# ----------------------------------------------------
# Projeto final Processamento de Linguagens
# Leonardo Filipe Lima Barroso, a100894
# Miguel Ângelo Martins Guimarães, a100837
# Pedro Andrade Carneiro, a100652
# ----------------------------------------------------

# Imports
import ply.lex as lex

######################## TOKENS ########################
# Tokens reservados
reserved = {
   'MOD'  : 'MOD',   # mod  - resto da divisao inteira 
   'EMIT' : 'EMIT',  # emit - dá print a um char (passa de int para char)
   'CHAR' : 'CHAR',  # char - declarar um caracter
   'DUP'  : 'DUP',   # dup  - duplicar valor na stack
   'SWAP' : 'SWAP',  # swap  - trocar os dois ultimos valores na stack
   'DROP' : 'DROP',  # drop  - retira o primeiro elem da stack
   'OVER' : 'OVER',  # over -  faz uma copia do segundo item e coloca no topo
   'ROT'  : 'ROT'    # rot -  coloca o terceiro item no topo
}

# Todos os tokens
tokens = (
    "MAIS",   # + - adição
    "MENOS",  # - - subtração
    "MUL",    # * -  multiplicação
    "DIV",    # / - divisão
    "PONTO",  # . - print do valor no topo da stack
    "COLON",  # : - inicio de uma função
    "SEMICOLON",  # ; - fim de função
    "LB",
    "RB",
    "NUM",
    "ID",
    "STRPRINT",  # ." txttxtxtxt txtxt" da print ao texto no interior
    "STRPRINT2", # .( txttxtxtxt txtxt) da print ao texto no interior mas transforma espaços consecutivos em um só espaço
    #"COMMENT",   # ( txtxt txtxt) é um comentario
    "QUOTE",    # "  - Usado para inicio de strings... etc
    "LETRA"
) + tuple(reserved.values())

######################## REGEX ########################
# Tokens
t_MAIS = r'\+'
t_MENOS = r"- " # Colado do lado esquerdo tem significado de negativo nos numeros
t_MUL = r'\*'
t_DIV = r'/'
t_PONTO = r'^\. |\s\.\s| \.$' # Print do valor no topo da stack (O ponto nunca esta colado a nada) (talvez com tab morra?)
t_COLON = r':'      # Inicio de função
t_SEMICOLON = r';'  # Fim de função
t_LB = r'\('
t_RB = r'\)'
t_STRPRINT  = r'\."\s[^"]+"'    # Da print a uma string
t_STRPRINT2 = r'\.\(\s[^\)]+\)' # Da print a uma string (mas transforma espaços consequtivos em um só)
t_QUOTE = r'\"'        # Usado em strings
t_LETRA = r'[A-Za-z]'  # Regex para reconhecer uma única letra

def t_NUM(t):
    r"(\+|-)?\d+"
    t.value = int(t.value)
    return t

# Nome de função
def t_ID(t):
    r'[A-Za-z_][A-Za-z_0-9]+'
    t.type = reserved.get(t.value.upper(),'ID') # Verificar se leu uma palavra reservada sem querer, senão valor default = VAR
    return t

t_ignore = ' \n\t\r'

def t_error(t):
    print(f"Carácter ilegal {t.value[0]}")
    t.lexer.skip(1)

######################## FIM ########################
lexer = lex.lex()