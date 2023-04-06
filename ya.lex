{(* Lexer para Gramática No. 2 - Expresiones aritméticas extendidas *)
}
(* Introducir cualquier header aqui *)

let delim = ["\s\t\n"]
let ws = delim+
let letter = ['A'-'C''a'-'b']
let digit = ['0'-'2']
let digits = digit+
let id = letter(letter|digit)*'()'letter(letter|digit)*


rule tokens = 
    ws        { return WHITESPACE }               (* Cambie por una acción válida, que devuelva el token *)
  | id        { return ID }
  | number    { return NUMBER }
  | '+'       { return PLUS }
  | '-'       { return MINUS }
  | '*'       { return TIMES }
  | '/'       { return DIV }
  | '('       { return LPAREN }
  | ')'       { return RPAREN }


  (* Introducir cualquier trailer aqui *)
  