from types import NoneType

import pytest

from pycli2._parser import ArgType, MapAction, get_argtype

SINGLE_ARG = None, None
SEQUNCEISH_ARG = "extend", "+"
MAPISH_ARG = MapAction, "+"


@pytest.mark.parametrize(
    "types, argtype",
    [
        # Base types
        ((str,), SINGLE_ARG),
        ((int,), SINGLE_ARG),
        ((bool,), SINGLE_ARG),
        ((float,), SINGLE_ARG),
        # Unions
        ((str, int, NoneType), SINGLE_ARG),
        # Tuples
        ((tuple,), SEQUNCEISH_ARG),
        ((tuple, NoneType), SEQUNCEISH_ARG),
        # Lists
        ((list,), SEQUNCEISH_ARG),
        ((list, NoneType), SEQUNCEISH_ARG),
        # Sets
        ((set,), SEQUNCEISH_ARG),
        ((set, NoneType), SEQUNCEISH_ARG),
        # Dicts
        ((dict,), MAPISH_ARG),
        ((dict, NoneType), MAPISH_ARG),
    ],
)
def test_correct_return(types: tuple[type, ...], argtype: ArgType) -> None:
    assert get_argtype(types) == argtype
