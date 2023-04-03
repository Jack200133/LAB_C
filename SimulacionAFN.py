import numpy as np
import pandas as pd

CEND = '\33[0m'
CRED = '\33[91m'
CYELLOW = '\33[93m'
CGREEM = '\33[92m'
CBLUE = '\33[94m'

# Funcion que regresa el conjunto de estados alcanzables por epsilon
def e_clouser(states):
    stack = []
    res = []
    for state in states:
        if state not in stack:
            stack.append(state)
            res.append(state)
        
    while len(stack) > 0:
        state = stack.pop()
        for i in afn['transition_function']:
            if i[0] == state and i[1] == 'ε':
                if i[2] not in res:
                    res.append(i[2])
                    stack.append(i[2])
    return res


# Funcion que regresa las posibles transiciones de un estado con un simbolo
def transition(q, a, tabla):
    qq = []
    for s in q :
       x = tabla[(tabla['q'] == s) & (tabla['a'] == a)]['d(q,a)']
       if(len(x) > 0):
           qq.append(x.values[0])
    return e_clouser(qq)

# Funcion que regresa el estado final alcanzable por un estado y una palabra
def final_state(q, w, tabla):
    n = len(w)
    if (n == 0):
        return e_clouser(q)
    else:
        a = (w[0])
        qq = transition(e_clouser(q), a, tabla)
        x = final_state(qq, w[1:], tabla)
        return x

# Funcion que regresa si una palabra es aceptada o no
def accepted(q, w, F, tab):
    x = final_state(q, w, tab)

    for i in x:
        if i in F:
            return print(CEND,'\nThe word',CGREEM,w,CEND,'is accepted\n\n')
    return print(CEND,'\nThe word',CRED,w,CEND,'is NOT accepted\n\n')

# Funcion que imprime el proceso de derivacion de una palabra
def derivation(q, w, tabla):
    n = len(w)
    if (n == 0):
        return print('\33[92m({},{})\33[93m => \33[94m{}'.format(q,'',q))
    else: 
        a = (w[0])
        q = e_clouser(q)
        qq = transition(q, a, tabla)
        x = derivation(qq, w[1:],tabla)
        return print('\33[92m({},{})\33[93m => \33[94m({},{})'.format(q,w,qq,w[1:]))

# Funcion que simula el funcionamiento de un AFN
def simularAFN(w,afn_r):
    global afn
    global table 
    afn = afn_r
    
    
    
    table = np.array(afn['transition_function'])
    tab = pd.DataFrame(data=table, columns=['q', 'a', 'd(q,a)'])
    #print(table)
    
    derivation(afn['start_states'], w, tab)
    accepted(afn['start_states'], w,afn['final_states'], tab)
