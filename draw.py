from graphviz import Digraph


def draw_afn(states, letters, transition_function, start_states, final_states, filename='AFN'):
    # Se crea el grafo
    dot = Digraph(comment='AFN')
    dot.attr(rankdir='LR')
    dot.attr('node', shape='circle')
    dot.node('', style='invisible')
    # Se agregan los estados
    for state in states:
        dot.node(state)
    # Se agrega la flecha de inicio
    for start_state in start_states:
        dot.edge('', start_state)
    
    # Se agregan las transiciones
    for transition in transition_function:
        dot.edge(transition[0], transition[2], label=transition[1])
    
    # Se agreg ael estado final
    for final_state in final_states:
        dot.node(final_state, shape='doublecircle')
    # Se muestra el grafo
    #dot.view(filename)
    dot.render(filename, format='png', view=True)
    return dot
