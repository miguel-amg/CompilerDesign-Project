import ply.lex as lex

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
)
t_POTENCIA = r'\*\*|\^'
t_MAIS = r'\+'
t_MENOS=r"\-"
t_MUL=r"\*"
t_DIV=r"\/"
t_PONTO=r"\."
t_LB=r"\("
t_RB=r"\)"
t_PERCENTAGEM=r"\%"



def t_NUM(t):
    r"\d+"
    t.value= int(t.value)
    return t

t_ignore = ' \n\t'

def t_error(t):
    print(f"Carácter ilegal {t.value[0]}")
    t.lexer.skip(1)


lexer = lex.lex()


data="""
2 3 + 4 5 * + .
"""

lexer.input(data)


while True:
    tok = lexer.token()
    if not tok: 
            break      # No more input
    print(tok)