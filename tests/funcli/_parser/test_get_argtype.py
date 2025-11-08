from types import NoneType

import pytest

from funcli._parser import ArgType, get_argtype

MONO_ARG = None, None
POLY_ARG = "extend", "+"


@pytest.mark.parametrize(
    "types, argtype",
    [
        # Base types
        ((str,), MONO_ARG),
        ((int,), MONO_ARG),
        ((bool,), MONO_ARG),
        ((float,), MONO_ARG),
        # Unions
        ((str, int, NoneType), MONO_ARG),
        # Tuples
        ((tuple,), POLY_ARG),
        ((tuple, NoneType), POLY_ARG),
        # Lists
        ((list,), POLY_ARG),
        ((list, NoneType), POLY_ARG),
        # Sets
        ((set,), POLY_ARG),
        ((set, NoneType), POLY_ARG),
        # Dicts
        ((dict,), POLY_ARG),
        ((dict, NoneType), POLY_ARG),
    ],
)
def test_correct_return(types: tuple[type, ...], argtype: ArgType) -> None:
    assert get_argtype(types) == argtype
