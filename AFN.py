import json
CEND = '\33[0m'
CRED = '\33[91m'
CYELLOW = '\33[93m'
CGREEM = '\33[92m'
CBLUE = '\33[94m'
# Tabla de símbolos operadores y AFN final
non_symbols = ['|', '*', '.', '(', ')', '+', '?']
afn = {}

# Tipos de operadores para el árbol de expresiones
class charType:
    SYMBOL = 1
    CONCAT = 2
    UNION  = 3
    KLEENE = 4
    KLEENE_PLUS = 5
    KLEENE_OPTIONAL = 6

# Clase para representar un estado
class afnState:
    def __init__(self):
        self.next_state = {}

# Clase para representar un AFN
class ExpressionTree():

    def __init__(self, charType, value=None):
        self.charType = charType
        self.value = value
        self.left = None
        self.right = None

# Creacion del arbol de expresiones
def make_exp_tree(regexp):
    # Pila de operadores y cola de salida
    stack = []
    # Para cada token en la expresión
    for c in regexp:
        # Si el token es una union
        if c == "|":
            #  Se crea un nodo con el operador OR
            z = ExpressionTree(charType.UNION,c)

            # Se asignan los hijos y se hacen dos pops de la pila
            z.right = stack.pop()
            z.left = stack.pop()
            # Se agrega el nodo a la pila
            stack.append(z)
        elif c == ".":
            # Se crea un nodo con la concatenacion
            z = ExpressionTree(charType.CONCAT,c)
            # Se asignan los hijos y se hacen dos pops de la pila
            z.right = stack.pop()
            z.left = stack.pop()
            # Se agrega el nodo a la pila
            stack.append(z)
        elif c == "*":
            # Se crea un nodo con el operador KLEENE
            z = ExpressionTree(charType.KLEENE,c)
            # Se asigna el hijo y se hace un pop de la pila
            z.left = stack.pop()
            # Se agrega el nodo a la pila
            stack.append(z)
        elif c == "+":
            # Se crea un nodo con el operador KLEENE PLUS
            z = ExpressionTree(charType.KLEENE_PLUS,c)
            # Se asigna el hijo y se hace un pop de la pila
            z.left = stack.pop() 
            # Se agrega el nodo a la pila
            stack.append(z)
        elif c == "?":
            # Se crea un nodo con el operador KLEENE OPTIONAL
            z = ExpressionTree(charType.KLEENE_OPTIONAL,c)
            # Se asigna el hijo y se hace un pop de la pila
            z.left = stack.pop() 
            # Se agrega el nodo a la pila
            stack.append(z)
        else:
            # Si no es un operador, se agrega a la pila
            stack.append(ExpressionTree(charType.SYMBOL, c))
    return stack[0]

# Funcion para generar el AFN
def compute_regex(exp_t):
    # Si el nodo es agregacion
    if exp_t.charType == charType.CONCAT:
        # Se llama a la funcion de agregacion
        return do_concat(exp_t)
    # Si el nodo es union
    elif exp_t.charType == charType.UNION:
        # Se llama a la funcion de union
        return do_union(exp_t)
    # Si el nodo es kleene
    elif exp_t.charType == charType.KLEENE:
        # Se llama a la funcion de kleene
        return do_kleene_star(exp_t)
    # Si el nodo es kleene plus
    elif exp_t.charType == charType.KLEENE_PLUS:
        # Se llama a la funcion de kleene plus
        return do_kleene_plus(exp_t)
    # Si el nodo es kleene optional
    elif exp_t.charType == charType.KLEENE_OPTIONAL:
        # Se llama a la funcion de kleene optional
        return do_kleene_optional(exp_t)
    else:
        # Si no es ninguno de los anteriores, se llama a la funcion de simbolos
        return eval_symbol(exp_t)

# Funcion para evaluar simbolos
def eval_symbol(exp_t):
    # Se crea un estado inicial y uno final
    start = afnState()
    end = afnState()
    # Se agrega la transicion del estado inicial al final
    start.next_state[exp_t.value] = [end]
    return start, end

# Funcion para evaluar agregaciones
def do_concat(exp_t):
    # Se llama a la funcion para evaluar los hijos
    left_afn  = compute_regex(exp_t.left)
    right_afn = compute_regex(exp_t.right)

    # Se agrega la transicion del estado final del hijo izquierdo al inicial del hijo derecho
    left_afn[1].next_state['ε'] = [right_afn[0]]
    return left_afn[0], right_afn[1]

# Funcion para evaluar uniones
def do_union(exp_t):
    # Se crea un estado inicial y uno final
    start = afnState()
    end = afnState()

    # Se llama a la funcion para evaluar los hijos
    first_afn = compute_regex(exp_t.left)
    second_afn = compute_regex(exp_t.right)

    # Se agregan las transiciones necesarias para la union
    start.next_state['ε'] = [first_afn[0], second_afn[0]]
    first_afn[1].next_state['ε'] = [end]
    second_afn[1].next_state['ε'] = [end]

    return start, end

# Funcion para evaluar kleene
def do_kleene_star(exp_t):
    # Se crea un estado inicial y uno final
    start = afnState()
    end = afnState()

    # Se llama a la funcion para evaluar el hijo
    starred_afn = compute_regex(exp_t.left)

    # Se agregan las transiciones necesarias para el kleene
    start.next_state['ε'] = [starred_afn[0], end]
    starred_afn[1].next_state['ε'] = [starred_afn[0], end]

    return start, end

# Funcion para evaluar kleene plus
def do_kleene_plus(exp_t):
    # Se crea un estado inicial y uno final
    start = afnState()
    end = afnState()

    # Se llama a la funcion para evaluar el hijo
    starred_afn = compute_regex(exp_t.left)

    # Se agregan las transiciones necesarias para el kleene plus
    start.next_state['ε'] = [starred_afn[0]]
    starred_afn[1].next_state['ε'] = [starred_afn[0], end]

    return start, end

def do_kleene_optional(exp_t):
    # Se crea un estado inicial y uno final
    start = afnState()
    end = afnState()

    # Se llama a la funcion para evaluar el hijo
    starred_afn = compute_regex(exp_t.left)

    # Se agregan las transiciones necesarias para el kleene optional
    start.next_state['ε'] = [starred_afn[0], end]
    starred_afn[1].next_state['ε'] = [end]

    return start, end

# Funcion crear las transiciones del AFN
def arrange_transitions(state, states_done, symbol_table,counter):
    global afn
    # Si el estado ya fue evaluado, se regresa
    if state in states_done:
        return
    # Si no, se agrega a la lista de estados evaluados
    states_done.append(state)

    # Se recorren los simbolos del estado
    for symbol in list(state.next_state):
        # Si el simbolo no esta en la lista de simbolos del AFN, se agrega
        if symbol not in afn['letters'] and symbol != 'ε':
            afn['letters'].append(symbol)
        # Se recorren los estados siguientes del simbolo
        for ns in state.next_state[symbol]:
            # Si el estado siguiente no esta en la tabla de simbolos, se agrega
            if ns not in symbol_table:
                # Se le asigna un numero de estado
                symbol_table[ns] = sorted(symbol_table.values())[-1] + 1
                q_state = "S" + str(symbol_table[ns]+counter)
                # Se agrega el estado al AFN
                afn['states'].append(q_state)
            # Se agrega la transicion al AFN
            afn['transition_function'].append(["S" + str(symbol_table[state]+counter), symbol, "S" + str(symbol_table[ns]+counter)])
        # Se llama a la funcion para evaluar los estados siguientes
        for ns in state.next_state[symbol]:
            arrange_transitions(ns, states_done, symbol_table,counter)

# Funcion para agregar el estado final del AFN
def final_st_afn():
    global afn
    # Se recorren los estados del AFN
    for st in afn["states"]:
        count = 0
        # Se recorren las transiciones del AFN
        for val in afn['transition_function']:
            # Se verifica si el estado tiene transiciones y no es el estado inicial
            if val[0] == st and val[2] != st:
                count += 1
        # Si el estado no tiene transiciones y no es el estado inicial, se agrega como estado final
        if count == 0 and st not in afn["final_states"]:
            afn["final_states"].append(st)

# Funcion para inicializar el AFN
def arrange_afn(fa,counter):
    global afn
    afn['states'] = []
    afn['letters'] = []
    afn['transition_function'] = []
    afn['start_states'] = []
    afn['final_states'] = []
    q_1 = "S" + str(counter+1)
    afn['states'].append(q_1)
    arrange_transitions(fa[0], [], {fa[0] : 1},counter)
    afn["start_states"].append(q_1)
    final_st_afn()

# Funcion para Guardar el AFN en un archivo JSON
def output_afn():
    global afn
    with open('AFN.json', 'w') as outjson:
        outjson.write(json.dumps(afn, indent = 4))

# Funcion para generar el AFN
def generate_afn(pr,counter =0):
    try:
        et = make_exp_tree(pr)
        fa = compute_regex(et)
        arrange_afn(fa,counter)
        output_afn()
        return afn
    except:
        print(CRED,'Expresión mal formada: token no reconocido',CEND,CYELLOW,pr,CEND)
        raise ValueError('Expresión mal formada: token no reconocido')