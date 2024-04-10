from anaLex import tokens
import ply.yacc as yacc


res={}
res["Total A Pagar"]=(0,0)


def p_tudo(p):
    "tudo : bloco tudo"
    p[0]=p[1]+p[2]

def p_tudo_empty(p):
    "tudo : empty"
    p[0]=""

def p_bloco(p):
    'bloco : CATEGORIA DOISPONTOS linha linhas'
    p[0]= p[1]+p[2]+"\n" +p[3]+p[4] +"\n"


def p_linhas(p):
    "linhas : linha linhas"
    p[0]=p[1]+p[2]

def p_linhas_empty(p):
    "linhas : empty"
    p[0]=""


def p_linha(p):
    "linha : INDICE QUATROPONTOS PRODUTO QUATROPONTOS PRECO QUATROPONTOS QUANTIDADE PONTOVIRGULA"
    res[p[3]]=(p[5],int(p[7]))
    valorTotal=res["Total A Pagar"][0]+(p[5]*int(p[7]))
    quantidadeTotal=res["Total A Pagar"][1]+int(p[7])
    res["Total A Pagar"]= (valorTotal,quantidadeTotal)
    p[0]=p[1]+p[2]+p[3]+p[4]+str(p[5])+p[6]+(p[7])+p[8]+"\n"

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    print("Erro sintático no input!")
    if p:
        print(f"Erro sintático na posição {p.lexpos}: token '{p.value}'")
    else:
        print("Erro sintático: fim inesperado do input")



# Build the parser
parser = yacc.yacc()

s = """

"""
result = parser.parse(s)
print(result)
for (a,b) in res.items():
    print(a,b)



# tudo: bloco tudo
#     | E 
#
# bloco: CATEGORIA DOISPONTOS linha linhas
#       
# linhas: linha linhas
#       | E
#
# linha: INDICE QUATROPONTOS PRODUTO QUATROPONTOS PRECO QUATROPONTOS QUANTIDADE PONTOVIRGULA