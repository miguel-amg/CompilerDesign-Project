1

0 = IF
        ." É zero!" CR
    ELSE
        ." Não é zero!" CR
    THEN

( TEM QUE DAR QUE NAO E ZERO)


    pusha if1
    call 

    if1:
        jz else1
        pushs "É zero"

    else1:
        pushs "Nao é zero"
        jz then1

    then1: