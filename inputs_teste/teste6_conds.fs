: func1 if ." Sucesso1" CR else ." Falha1" CR then ;
1 func1

: func2 if ." Falha2" CR else ." Sucesso2" CR then ;
0 func2

: func3 if ." Sucesso3" CR then ;
1 func3

: func4 if ." Falha4" CR then ." Sucesso4" CR ; 
0 func4

: func5 if if ." Sucesso5" CR else ." Falha5" CR then ." Sucesso5" CR then ." Sucesso5" CR ;
1 1 func5

