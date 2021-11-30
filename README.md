# pylox
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/sco1-pylox)](https://pypi.org/project/sco1-pylox/)
[![PyPI - Version](https://img.shields.io/pypi/v/sco1-pylox)](https://pypi.org/project/sco1-pylox/)
[![PyPI - License](https://img.shields.io/pypi/l/sco1-pylox?color=magenta)](https://github.com/sco1/sco1-pylox/blob/main/LICENSE)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/sco1/pylox/main.svg)](https://results.pre-commit.ci/latest/github/sco1/pylox/main)
[![Code style: black](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)
[![Open in Visual Studio Code](https://open.vscode.dev/badges/open-in-vscode.svg)](https://open.vscode.dev/sco1/pylox)

## Introduction
This is my Python implementation of an interpreter for the Lox programming language from Robert Nystrom's *[Crafting Interpreters](https://craftinginterpreters.com/)*.

## Python?
While the text is implemented in Java and C as its high & low-level implementations, I have no idea how to write either of them! Instead, I'll be using Python for the high-level implementation & eventually Rust for the low-level imeplementation.

## Differences From Text
For the sake of fitting within a decently sized text, the fully implemented Lox spec omits features that users of other programming languages may miss. Often these are discussed as notes within a chapter, or presented as challenges at the end of a chapter. Significant difference in this implementation from the text reference are noted below.
### Defined by Challenges
  * (Chapter 4): Arbitrarily nested block comments (`/* ... */`)
  * (Chapter 9): `break` statements are available for `for` and `while` loops
### User Choice
  * Division by zero returns `NaN` (Python's `float('nan')`)
  * Strings may be defined using either `"` or `'`
  * Modulo operator (`%`)
  * Power operator (`^`)
  * Integer division operator (`\`)
  * Both floats and integers are represented
    * Return type from operations follows Python3's semantics
  * Containers
    * `array()`

### Additional Built-ins:
Unless otherwise noted, behavior mirrors the similarly named Python function
  * `abs`
  * `ceil`
  * `divmod`
  * `floor`
  * `input`
  * `len`
  * `max`
  * `mean`
  * `median`
  * `min`
  * `mode`
  * `ord`
  * `read_text` (via `pathlib.Path.read_text`)
  * `std`
  * `string_array`
    * Gives a `LoxArray` whose contents are equivalent to `collections.deque(<some string>)`
