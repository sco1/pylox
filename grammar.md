# Grammar Specification
```
expression: equality
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
```

## Notes
### Metasyntax
* Capitalized terminals indicate lexemes whose text representation may vary (e.g. `NUMBER` could be `123`, `12.34`, etc.)
