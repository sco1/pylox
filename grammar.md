# Grammar Specification
```
expression:
    | literal
    | unary
    | binary
    | grouping
literal:
    | NUMBER
    | STRING
    | "true"
    | "false"
    | "nil"
grouping: "(" expression ")";
unary: ( "-" | "!" ) expression;
binary: expression operator expression
operator:
    | "=="
    | "!="
    | "<"
    | "<="
    | ">"
    | ">="
    | "+"
    | "-"
    | "*"
    | "/"
```

## Notes
### Metasyntax
* Capitalized terminals indicate lexemes whose text representation may vary (e.g. `NUMBER` could be `123`, `12.34`, etc.)
