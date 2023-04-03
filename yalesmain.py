import re
from yalex import *
yalex_content = '''
{
    header information
}

let digit   = ["0" - "9"]
let letter  = ["a" - "z" "A" - "Z"]

rule tokens =
  '"'                { STRING }
  | "'"              { CHAR }
  | letter+          { IDENTIFIER }
  | digit+           { NUMBER }
  | " "              { WHITESPACE }
'''

header_result = ''
regex = {}
simple_pattern = r"\[(\w)\s*-\s*(\w)\]"
compound_pattern = r"\[(\w)\s*-\s*(\w)\s*(\w)\s*-\s*(\w)\]"
simple_regex_pattern = r"^let\s+\w+\s+=\s+(.*?)$"

# Llamando a las funciones en orden
file_content = yalex_content

header_result = build_header(file_content)
file_content = clean_comments(file_content)
file_content = replace_quotation_mark(file_content)
regex = build_regex(file_content)
tokens = build_tokens(file_content, regex)

# Imprimir resultados
print("Header:")
print(header_result)
print("\nTokens:")
for token in tokens:
    print(token)
