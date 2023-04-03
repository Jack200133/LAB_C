from newpostfix import shunting_yard
from AFN import generate_afn
from draw import draw_afn
from SimulacionAFN import simularAFN



CEND = '\33[0m'
CRED = '\33[91m'
CYELLOW = '\33[93m'
CGREEM = '\33[92m'
CBLUE = '\33[94m'

reg = "(a*(b|a)*)|(qtq)*"
postfix = shunting_yard(reg)
print('\33[93mPOSTFIX: ',postfix,'\33[94m')
afn = generate_afn(postfix)
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

print('\033[0m')

afd = generate_afd()
print(CRED,'\n\n-------------------',CEND,CYELLOW,'AFD',CEND,CRED,'-------------------\n')
print ('Alfabeto: ', CGREEM, afd['alphabet'], CRED )
print ('Estado inicial: ', CGREEM, afd['start_stateB'], CRED )
print ('Estados de aceptación: ', CGREEM, afd['final_statesB'], CRED )
print ('Estados: ', CGREEM, afd['statesB'], CRED )
print ('Transiciones: ')
for inicial, simbolo,final in afd['transitionB']:
    print(CGREEM, inicial, CYELLOW, '==', CBLUE, F"({simbolo})",CYELLOW, '==>',CGREEM,final,CRED)
draw_afn(afd['statesB'], afd['alphabet'], afd['transitionB'], afd['start_stateB'], afd['final_statesB'],filename='AFD')

miniAFD = build_miniAFD(afd)
print(CRED,'\n\n-----------------',CEND,CYELLOW,'AFD MINIMIZADO',CEND,CRED,' -------------------\n')
print('Estado inicial: ',CGREEM,miniAFD['statesB'],CRED)
print('Estado de aceptacion: ',CGREEM,miniAFD['alphabet'],CRED)
print('Estados: ',CGREEM,miniAFD['start_stateB'],CRED)
print('Alfabeto: ',CGREEM,miniAFD['final_statesB'],CRED)

for inicial, simbolo, final in miniAFD['transitionB']:
    print(CGREEM,inicial,CYELLOW,'==',CBLUE,F"({simbolo})",CYELLOW,'==>',CGREEM,final,CRED)

draw_afn(miniAFD['statesB'], miniAFD['alphabet'], miniAFD['transitionB'], miniAFD['start_stateB'], miniAFD['final_statesB'],filename='AFDminimizado')


print(CRED,'\n\n-----------', CYELLOW,'Simulacion AFN',CRED ,'-----------\n')
simularAFN('aaac',afn)


print(CRED,'\n\n-----------', CYELLOW,'Simulacion AFD',CRED ,'-----------')
simularAFD('aaac',afd['transitionB'],afd['final_statesB'])
