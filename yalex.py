import re

def format_yalex_content(yalex_content):
    file_content = yalex_content
    header_result, file_content = build_header_and_trailer(file_content)
    file_content = clean_comments(file_content)
    file_content = replace_quotation_mark(file_content)
    regex = build_regex(file_content)
    tokens = build_tokens(file_content, regex)
    return header_result, regex, tokens

def replace_quotation_mark(file_content):
    file_content = file_content.replace('"', " ' ")
    file_content = file_content.replace("'", " ' ")
    return file_content

def clean_comments(file_content):
    patron = re.compile(r'\(\*.*?\*\)', re.DOTALL)
    file_content = re.sub(patron, '', file_content)
    return file_content

def build_regex(file_content,inicio):
    ErrorStack = []
    patron = re.compile(r'\{.*?\}', re.DOTALL)
    content = re.sub(patron, '', file_content)
    content = content.split("\n")
    simple_pattern = r"\[(\w)\s*-\s*(\w)\]"
    compound_pattern = r"\[(\w)\s*-\s*(\w)\s*(\w)\s*-\s*(\w)\]"
    simple_regex_pattern = r"^let\s+\w+\s+=\s+(.*?)$"
    regex = {}

    # Verificar llaves y paréntesis desbalanceados
    open_brackets = ['{', '(']
    close_brackets = ['}', ')']
    stack = []

    for line_num, line in enumerate(content, start=1):
        for char in line:
            if char in open_brackets:
                stack.append((char, line_num))
            elif char in close_brackets:
                if not stack or stack[-1][0] != open_brackets[close_brackets.index(char)]:
                    ErrorStack.append(f"Llaves o paréntesis desbalanceados en la línea {line_num+inicio}: {line}")
                    break
                else:
                    stack.pop()

        line = line.strip()
        if line:
            if re.match(simple_regex_pattern, line):
                regex = add_common_regex(line, regex, simple_pattern, compound_pattern)
            elif line.startswith("let"):
                ErrorStack.append(f"Expresión regular inválida en la línea {line_num+inicio}: {line}")

    if stack:
        for bracket, line_num in stack:
            ErrorStack.append(f"Llave o paréntesis '{bracket}' sin cerrar en la línea {line_num+inicio}")

    return regex, ErrorStack


def build_tokens(file_content, regex):
    content = file_content.split('rule tokens =')
    content = trim_quotation_marks(content[1])
    content = content.strip().split('|')
    content = replace_delimiters(content)
    content = convert_regexes_to_tuples(content)
    content = add_meta_character_token(content)
    content = replace_existing_regex(content, regex)
    return content

def build_header_and_trailer(file_content):
    content = file_content.split('\n')
    header_result = ''
    trailer_result = ''
    i = 0

    # Build header
    if check_header(content):
        finished = False
        while not finished:
            line = content[i].strip()
            for element in line:
                if element != '{' and element != '}':
                    header_result += element
                if element == '}':
                    finished = True
                    header_result = header_result.strip()
                    break
            header_result += '\n'
            i += 1

    file_content = '\n'.join(content[i:])

    # Build trailer
    content = file_content.split('\n')
    j = len(content) - 1
    if check_trailer(content):
        finished = False
        while not finished:
            line = content[j].strip()
            for element in line:
                if element != '{' and element != '}':
                    trailer_result = element + trailer_result
                if element == '{':
                    finished = True
                    trailer_result = trailer_result.strip()
                    break
            trailer_result = '\n' + trailer_result
            j -= 1

    file_content = '\n'.join(content[:j+1])
    trailer_result = trailer_result[::-1]
    return header_result, trailer_result, file_content, i


def check_trailer(content):
    has_header = True
    j = len(content) - 1
    while has_header:
        line = content[j].strip()
        if line:
            if 'return' in line or '|' in line:
                return False
            if line == "}" or "}" in line:
                return True
        j -= 1


def check_header(content):
    has_header = True
    i = 0
    while has_header:
        line = content[i].strip()
        if line:
            if line == "{" or "{" in line:
                return True
        if 'let' in line or 'rule' in line:
            return False
        i += 1

# Funciones auxiliares para build_tokens

def replace_delimiters(expressions):
    new_list = []
    for element in expressions:
        element = element.replace('\n', '')
        element = element.strip()
        new_list.append(element)
    return new_list

def replace_existing_regex(expressions, regex):
    new_list = []
    for element in expressions:
        r = element[0]
        if r in regex:
            replacement = regex[r]
            element[0] = replacement
        new_list.append(element)
    return new_list

def convert_regexes_to_tuples(expressions):
    new_list = []
    for element in expressions:
        splitted = element.split('\t', maxsplit=1)
        if len(splitted) >= 2:
            first_part = splitted[0]
            if first_part not in regex:
                first_part = common_regex(first_part.split(" "))
            second_part = splitted[1].replace('\t', '')
            second_part = second_part.replace('{' , '')
            second_part = second_part.replace('}', '')
            second_part = second_part.strip()
            element = [first_part, second_part]
            new_list.append(element)
    return new_list


def add_meta_character_token(expressions):
    new_list = []
    for element in expressions:
        expression = element[0]
        if "'" in expression or '"' in expression:
            element[0] = add_meta_character_string(expression)
        new_list.append(element)
    return new_list

def trim_quotation_marks(line):
    matches = re.findall(r"'([^']+)'", line)
    for element in matches:
        text = element
        line = line.replace("'" + text + "'", "'" + text.strip() + "'")
    return line

# Funciones auxiliares para add_common_regex

def space_operators(line):
    operators = '*+|?()'
    for operator in operators:
        line = line.replace(operator, ' ' + operator + ' ')
    return line

def replace_common_patterns(regex, simple_pattern, compound_pattern):
    search_simple_regex_result = re.search(simple_pattern, regex)
    search_compound_regex_result = re.search(compound_pattern, regex)
    
    letters = 'abcdefghijklmnopqrstuvwxyz'
    upper_letters = letters.upper()
    numbers = '0123456789'

    if search_simple_regex_result and not search_compound_regex_result:
        regex = simple_range(regex, search_simple_regex_result, letters, numbers,upper_letters)
    elif search_compound_regex_result:
        regex = compound_range(regex, search_compound_regex_result, letters, numbers,upper_letters)

    return regex

def simple_range(regex, search_simple_regex_result, letters, numbers,upper_letters):
    initial = search_simple_regex_result.group(1)
    final = search_simple_regex_result.group(2)
    result = replace_range(initial, final, letters, numbers,upper_letters)
    result = '(' + result + ')'
    regex = regex.replace('['+initial+'-'+final+']', result)
    return regex

def compound_range(regex, search_compound_regex_result, letters, numbers,upper_letters):
    first_initial = search_compound_regex_result.group(1)
    first_final = search_compound_regex_result.group(2)

    last_initial = search_compound_regex_result.group(3)
    last_final = search_compound_regex_result.group(4)

    first_range = replace_range(first_initial, first_final, letters, numbers,upper_letters)
    second_range = replace_range(last_initial, last_final, letters, numbers,upper_letters)

    result = '(' + first_range + '|' + second_range + ')'
    replaced = ''
    i = 0
    closed = False
    while not closed:
        if regex[i] == ']':
            closed = True
        replaced += regex[i]
        i += 1
    regex = regex.replace(replaced, result)
    return regex

def replace_range(initial, final, letters, numbers,upper_letters):
    result = str(initial) + '|'
    if initial.lower() in numbers and final.lower() in letters:
        result += get_range_of_numbers(initial, '9') + '|'
        initial_letter = 'A' if final in upper_letters else 'a'
        result += initial_letter + '|'
        result += get_range_of_strings(initial_letter, final, letters)
    elif initial.lower() in letters:
        final_letter = 'Z' if initial in upper_letters else 'z'
        if final in numbers:
            result += get_range_of_strings(initial, final_letter, letters) + '|'
            result += '0' + '|' + get_range_of_numbers('0', final)
        else:
            result += get_range_of_strings(initial, final, letters)
    elif initial in numbers:
            result += get_range_of_numbers(initial, final)
    return result

def get_range_of_strings(initial, final, letters):
    result = ''
    if ord(initial) > ord(final) and final.lower() in letters:
        result += get_range_of_strings(initial, 'z', letters) + '|'
        result += get_range_of_strings(chr(ord(initial.upper()) -1), final, letters)
    else:
        for i in range(ord(initial) + 1, ord(final)):
            between_letter = chr(i)
            result += between_letter + '|'
        result += final
    return result

def get_range_of_numbers(initial, final):
    result = ''
    for i in range(int(initial) + 1, int(final)):
        result += str(i) + '|'
    result += final
    return result


def common_regex(line, regex, simple_pattern, compound_pattern):
    body = build_common_regex(line, regex)
    body = body.replace('ε', ' ')
    body = replace_common_patterns(body, simple_pattern, compound_pattern)
    body = body.strip()
    return body

def add_common_regex(line, regex, simple_pattern, compound_pattern):
    line = space_operators(line)
    line = trim_quotation_marks(line)
    line = line.replace('" "', '"ε"')
    line = line.replace("' '", "'ε'")
    line = line.split(" ")
    body = common_regex(line[3:], regex, simple_pattern, compound_pattern)
    regex[line[1]] = body
    return regex

def build_common_regex(line, regex):
    body = ''
    for i in range(len(line)):
        element = line[i]
        if "'" in element or '"' in element:
            if 'space' == element:
                body += ' '
            else:
                element = element.replace('"', '')
                element = element.replace("'", "")
                element = element.replace('+', '\+')
                element = element.replace('.', '\.')
                element = element.replace('*', '\*')
                element = element.replace('(', '\(')
                element = element.replace(')', '\)')
                body += element
        elif not check_operators(element) and len(element) > 1:
            replacement = regex[element]
            body += replacement
        else:
            body += element
    return body

def check_operators(element):
    operators = '*+|?'
    for operator in operators:
        if operator in element:
            return True
    return False

def add_meta_character_string(expression):
    expression = expression.replace('.', '\.')
    expression = expression.replace('+', '\+')
    expression = expression.replace('*', '\*')
    expression = expression.replace('"', '')
    expression = expression.replace("'", "")
    return expression
