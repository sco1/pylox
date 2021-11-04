import typing as t

import pytest

from pylox.interpreter import is_truthy, stringify


TRUTHINESS_TEST_CASES = [
    (None, False),
    (False, False),
    (True, True),
    (1, True),
    (1.0, True),
    (0, True),
    (0.0, True),
]


@pytest.mark.parametrize(("in_val", "truth_out"), TRUTHINESS_TEST_CASES)
def test_is_truthy(in_val: t.Any, truth_out: bool) -> None:
    assert is_truthy(in_val) == truth_out


STRINGIFY_TEST_CASES = [
    (None, "nil"),
    (False, "False"),
    (True, "True"),
    (1.0, "1.0"),
    ("hi", "hi"),
]


@pytest.mark.parametrize(("in_val", "truth_out"), STRINGIFY_TEST_CASES)
def test_stringify(in_val: t.Any, truth_out: str) -> None:
    assert stringify(in_val) == truth_out
