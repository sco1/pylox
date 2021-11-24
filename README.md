# pylox
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)
[![Open in Visual Studio Code](https://open.vscode.dev/badges/open-in-vscode.svg)](https://open.vscode.dev/sco1/pylox)

## Introduction
This is my Python implementation of an interpreter for the Lox programming language from Robert Nystrom's *[Crafting Interpreters](https://craftinginterpreters.com/)*.

## Python?
While the text is implemented in Java and C as its high & low-level implementations, I have no idea how to write either of them! Instead, I'll be using Python for the high-level implementation & eventually Rust for the low-level imeplementation.

## Differences From Text
For the sake of fitting within a decently sized text, the fully implemented Lox spec omits features that users of other programming languages may miss. Often these are discussed as notes within a chapter, or presented as challenges at the end of a chapter. Significant difference in this implementation from the text reference are noted below.
### Defined by Challenges
  * (Chapter 9): `break` statements are available for `for` and `while` loops
### User Choice
  * Division by zero returns `NaN` (Python's `float('nan')`)
  * Strings may be defined using either `"` or `'`
  * Modulo operator (`%`)
  * Power operator (`^`)
  * Integer division operator (`\`)
  * Both floats and integers are represented
    * Returns from operations between mismatched types follow Python's semantics

### Additional Built-ins:
  * `abs`
  * `ceil`
  * `floor`
  * `max`
  * `min`
