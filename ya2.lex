{(* Lexer para Gramática No. 2 - Expresiones aritméticas extendidas *)}
(* Introducir cualquier header aqui *)

let delim = ["\s\t\n"]
let ws = delim+
let letter = ['D'-'R''a'-'c']
let digit = ['3'-'8']
let digits = digit+

rule tokens = 
    ws        { return WHITESPACE }               (* Cambie por una acción válida, que devuelva el token *)
  | digits    { return NUMBER }
  | '+'       { return PLUS }
  | '-'       { return MINUS }
  | '*'       { return TIMES }
  | '/'       { return DIV }
  | '('       { return LPAREN }
  | ')'       { return RPAREN }


{ (* Introducir cualquier código de inicialización aqui *)  }
  