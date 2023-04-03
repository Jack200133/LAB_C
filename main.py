from newpostfix import shunting_yard
from AFN import generate_afn
from draw import draw_afn
from SimulacionAFN import simularAFN



CEND = '\33[0m'
CRED = '\33[91m'
CYELLOW = '\33[93m'
CGREEM = '\33[92m'
CBLUE = '\33[94m'

reg = "(ab)*|(a)bb(a/*)(a)"
                

postfix = shunting_yard(reg)
print('\33[93mPOSTFIX: ',postfix,'\33[94m')
afn = generate_afn(postfix,1)
print(CRED,'\n\n-----------------',CEND,CYELLOW,'AFN',CEND,CRED,' -------------------')
afn = generate_afn(postfix)
print('Estado inicial: ',CGREEM,afn['start_states'],CRED)
print('Estado de aceptacion: ',CGREEM,afn['final_states'],CRED)
print('Estados: ',CGREEM,afn['states'],CRED)
print('Alfabeto: ',CGREEM,afn['letters'],CRED)
print('Transiciones: ')
for inicial, simbolo, final in afn['transition_function']:
    print(CGREEM,inicial,CYELLOW,'==',CBLUE,F"({simbolo})",CYELLOW,'==>',CGREEM,final,CRED)
draw_afn(afn['states'], afn['letters'], afn['transition_function'], afn['start_states'], afn['final_states'])