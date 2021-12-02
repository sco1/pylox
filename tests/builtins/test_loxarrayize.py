import typing as t
from collections import deque

import pytest

from pylox.builtins.py_builtins import LoxArray, _lox_arrayize

IN_ITERS = [
    ("abc123", deque("abc123")),
    ([], deque([])),
    ([1, 2, 3], deque([1, 2, 3])),
]


@pytest.mark.parametrize(("in_iter", "truth_deque"), IN_ITERS)
def test_lox_arrayize(in_iter: t.Iterable, truth_deque: deque) -> None:
    arr = _lox_arrayize(in_iter)

    assert isinstance(arr, LoxArray)
    assert arr.fields == truth_deque
