from types import NoneType

import pytest

from funcli._parser import get_types


@pytest.mark.parametrize(
    "annotation, types",
    [
        # Base types
        (str, (str,)),
        (int, (int,)),
        (bool, (bool,)),
        (float, (float,)),
        # Unions
        (str | int | None, (str, int, NoneType)),
        # Tuples
        (tuple, (tuple,)),
        (tuple[str | int], (tuple,)),
        (tuple[str | int] | None, (tuple, NoneType)),
        # Lists
        (list, (list,)),
        (list[str | int], (list,)),
        (list[str | int] | None, (list, NoneType)),
        # Sets
        (set, (set,)),
        (set[str | int], (set,)),
        (set[str | int] | None, (set, NoneType)),
        # Dicts
        (dict, (dict,)),
        (dict[str, int], (dict,)),
        (dict[str, int] | None, (dict, NoneType)),
    ],
)
def test_correct_return(annotation: type, types: tuple[type, ...]) -> None:
    assert get_types(annotation) == types
