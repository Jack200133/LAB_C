import re
from yalex import *
from AFN import generate_afn,add_new_initial_state,merge_automata
from draw import draw_afn

CEND = '\33[0m'
CRED = '\33[91m'
CYELLOW = '\33[93m'
CGREEM = '\33[92m'
CBLUE = '\33[94m'

with open('ya.lex', 'r') as f:
    # Leer todas las líneas del archivo
    yalex_content = f.read()


header_result = ''
regex = {}
simple_pattern = r"\[(\w)\s*-\s*(\w)\]"
compound_pattern = r"\[(\w)\s*-\s*(\w)\s*(\w)\s*-\s*(\w)\]"
simple_regex_pattern = r"^let\s+\w+\s+=\s+(.*?)$"

# Llamando a las funciones en orden
file_content = yalex_content

header_result, trailer_result, file_content,i = build_header_and_trailer(file_content)
file_content = clean_comments(file_content)
file_content = replace_quotation_mark(file_content)
regex,errorStack = build_regex(file_content,i)
tokens = build_tokens(file_content, regex)

if errorStack:
    print("Error stack:")
    for error in errorStack:
        print(error)
    exit()

# Imprimir resultados
print("Header:")
print(header_result)
print("\nTokens:")
for token in tokens:
    print(token)
print("\nRegex:")
for key, value in regex.items():
    print(key, ":", value)
print("\nTrailer:")
print(trailer_result)


# ARMAR MEGAAUTOMATA CON LOS REGEX Y AFNS
i = 0

regexAFN = {}
for key, value in regex.items():
    # Generar AFN para cada regex
    afn = {}
    afn = generate_afn(value,i)
    i =afn['final_states'][0][1:]
    regexAFN[key] = afn

    print('Estado inicial: ',CGREEM,afn['start_states'],CRED)
    print('Estado de aceptacion: ',CGREEM,afn['final_states'],CRED)
    print('Estados: ',CGREEM,afn['states'],CRED)
    print('Alfabeto: ',CGREEM,afn['letters'],CRED)
    print('Transiciones: ')
    for inicial, simbolo, final in afn['transition_function']:
        print(CGREEM,inicial,CYELLOW,'==',CBLUE,F"({simbolo})",CYELLOW,'==>',CGREEM,final,CRED)
    draw_afn(afn['states'], afn['letters'], afn['transition_function'], afn['start_states'], afn['final_states'],key)
print(regexAFN,'\n\n')



automata_list = list(regexAFN.values())

# Unir todos los autómatas en la lista
merged_automaton = automata_list[0]
for i in range(1, len(automata_list)):
    merged_automaton = merge_automata(merged_automaton, automata_list[i])

# Agregar el nuevo estado inicial 's0' con transiciones epsilon a los estados iniciales
initial_states = [automaton["start_states"][0] for automaton in automata_list]
final_automaton = add_new_initial_state(merged_automaton, initial_states)

# Imprimir el autómata resultante
print(final_automaton)
print('Estado inicial: ',CGREEM,final_automaton['start_states'],CRED)
print('Estado de aceptacion: ',CGREEM,final_automaton['final_states'],CRED)
print('Estados: ',CGREEM,final_automaton['states'],CRED)
print('Alfabeto: ',CGREEM,final_automaton['letters'],CRED)
print('Transiciones: ')
for inicial, simbolo, final in final_automaton['transition_function']:
    print(CGREEM,inicial,CYELLOW,'==',CBLUE,F"({simbolo})",CYELLOW,'==>',CGREEM,final,CRED)
draw_afn(final_automaton['states'], final_automaton['letters'], final_automaton['transition_function'], final_automaton['start_states'], final_automaton['final_states'],'final_automaton')