# pylox
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/sco1-pylox/0.5.2?logo=python&logoColor=FFD43B)](https://pypi.org/project/sco1-pylox/)
[![PyPI](https://img.shields.io/pypi/v/sco1-pylox?logo=Python&logoColor=FFD43B)](https://pypi.org/project/sco1-pylox/)
[![PyPI - License](https://img.shields.io/pypi/l/sco1-pylox?color=magenta)](https://github.com/sco1/sco1-pylox/blob/main/LICENSE)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/sco1/pylox/main.svg)](https://results.pre-commit.ci/latest/github/sco1/pylox/main)

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
  * A basic `include` header system
    * Supports "stdlib" imports (`<header_name>`) and path imports (`"path/to/file"`)
    * Recursive `include` not supported
    * Imported source assumed to be valid code

### Additional Built-ins:
Unless otherwise noted, behavior mirrors the similarly named Python function.

#### General
  * `input`
  * `len`
  * `ord`
  * `read_text` (via `pathlib.Path.read_text`)
  * `str2num`
  * `string_array`
    * Gives a `LoxArray` whose contents are equivalent to `collections.deque(<some string>)`

#### Math
  * `abs`
  * `ceil`
  * `divmod`
  * `floor`
  * `max`
  * `min`

#### Regex
For methods whose Python equivalent returns [Match objects](https://docs.python.org/3/library/re.html#match-objects), a `LoxArray` is returned. The first value in the array will always correspond to `match.group(0)`; if the pattern contains one or more groups then the array will match the output of `match.groups()`

  * `re_findall`
  * `re_match`
  * `re_search`
  * `re_sub`

#### Stats
  * `mean`
  * `median`
  * `mode`
  * `std`

### Pure lox headers
  * `<array_sum>`
  * `<hello_world>`
  * `<map>`
  * `<split_on>`
