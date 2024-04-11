# ----------------------------------------------------
# Projeto final Processamento de Linguagens
# Leonardo Filipe Lima Barroso, a100894
# Miguel Ângelo Martins Guimarães, a100837
# Pedro Andrade Carneiro, a100652
# ----------------------------------------------------

# Testador do programa anaLex.py

# Uso do programa:
# Ir inserindo as expressões manualmente e clicando enter.
# Alternativamente poderá ser inserido um ficheiro atráves do comando:
# python3 lexTester.py < testFile.txt 

# Imports
import anaLex
import sys

#################################### BOAS-VINDAS ####################################
print(
"""-------------------------------------
Aplicação de debug
Testador do analisador lexico
-------------------------------------
""")

####################################  CODIGO  ####################################
# Iterar o input do stdin
for line in sys.stdin:
    anaLex.lexer.input(line)

    while True: 
        tok = anaLex.lexer.token()
        if not tok: 
            break # Sem mais input
        print(tok)