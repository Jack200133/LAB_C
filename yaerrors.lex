
let delim = ["\s\t\n"]
let ws hola = delim+
let letter = ['D'-'R''a'-'c']
let digit = ['3'-'8']
let digits = digit+
}
rule tokens = 
    ws        { return WHITESPACE }               (* Cambie por una acción válida, que devuelva el token *)
  | digits    { return NUMBER }
  | '+'       { return PLUS }
  | '-'       { return MINUS }
  | '*'       { return TIMES }
  | '/'       { return DIV }
  | '('       { return LPAREN }
  | ')'       { return RPAREN }
