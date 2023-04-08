(* Lexer para Gramática No. 2 *)

(* Introducir cualquier header aqui *)

let delim = (' ''\t''\n')
let ws = delim+
let letter = ['A'-'Z''a'-'z']
let str = (_)*
let digit = ['0'-'9']
let digits = digit+
let id = letter(letter|str|digit)*
let number = digits('.'digits)?('E'['+''-']?digits)?

rule tokens = 
    ws
  | id        { return ID }               (* Cambie por una acción válida, que devuelva el token *)
  | number    { return NUMBER }
  | ';'       { return SEMICOLON }
  | ":="      { return ASSIGNOP }
  | '<'       { return LT }
  | '='       { return EQ }
  | '+'       { return PLUS }
  | '-'       { return MINUS }
  | '*'       { return TIMES }
  | '/'       { return DIV }
  | '('       { return LPAREN }
  | ')'       { return RPAREN }

(* Introducir cualquier trailer aqui *)