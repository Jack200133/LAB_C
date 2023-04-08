(* Lexer para Gramática No. 1 - Expresiones aritméticas simples para variables *)
{(* Introducir cualquier header aqui *)}

let delim = [' ''\t''\n']
let ws = delim+
let letter = ['A'-'Z''a'-'z']
let digit = ['0'-'9']
let id = letter(letter|digit)*

rule tokens = 
    ws
  | id        { return ID }               (* Cambie por una acción válida, que devuelva el token *)
  | '+'       { return PLUS }
  | '*'       { return TIMES }
  | '('       { return LPAREN }
  | ')'       { return RPAREN }

(* Introducir cualquier trailer aqui *)