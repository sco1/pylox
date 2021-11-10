# Grammar Specification
```
program: declaration* EOF
declaration:
    | varDecl
    | statement
varDecl: "var" IDENTIFIER ( "=" expression )? ";"
statement:
    | exprStmt
    | forStmt
    | ifStmt
    | printStmt
    | whileStmt
    | block
exprStmt: expression ";"
forStmt: "for" "(" ( varDecl | exprStamt | ";" ) expression? ";" expression? ")" statement
ifStmt: "if" "(" expression ")" statement ( "else" statement )?
printStmt: "print" expression ";"
whileStmt: "while" "(" expression ")" statement
block: "{" declaration* "}"
expression: assignment
assignment:
    | IDENTIFIER = assignment
    | logic_or
logic_or: logic_and ( "or" logic_and )*
logic_and: equality ( "and" equality )*
equality: comparison ( ( "!=" | "==" ) comparison )*
comparison: term ( ( ">" | ">=" | "<" | "<=" ) term )*
term: factor ( ( "-" | "+" ) factor )*
factor: power ( ( "/" | "*" | "%") power )*
power: unary ( ( "^" ) unary)*
unary:
    | ( "!" | "-" ) unary
    | primary
primary:
    | NUMBER
    | STRING
    | "true"
    | "false"
    | "nil"
    | "(" expression ")"
    | IDENTIFIER
```

## Notes
### Metasyntax
* Capitalized terminals indicate lexemes whose text representation may vary (e.g. `NUMBER` could be `123`, `12.34`, etc.)
