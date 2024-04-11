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
   'CHAR' : 'CHAR',
}

# Todos os tokens
tokens = (
    "POTENCIA",
    "MAIS",
    "MENOS",
    "MUL",
    "DIV",
    "PONTO",
    "LB",
    "RB",
    "PERCENTAGEM",
    "NUM"
) + tuple(reserved.values())

######################## REGEX ########################
# Tokens
t_POTENCIA = r'\*\*|\^'
t_MAIS = r'\+'
t_MENOS = r"\-"
t_MUL = r"\*"
t_DIV = r"\/"
t_PONTO = r"\." # Print do valor no topo da stack
t_LB = r"\("
t_RB = r"\)"
t_PERCENTAGEM = r"\%"

def t_NUM(t):
    r"\d+"
    t.value = int(t.value)
    return t

t_ignore = ' \n\t\r'

def t_error(t):
    print(f"Carácter ilegal {t.value[0]}")
    t.lexer.skip(1)

######################## FIM ########################
lexer = lex.lex()