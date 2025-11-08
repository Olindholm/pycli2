import inspect
from collections.abc import Sequence
from typing import Any

import pytest
from pytest import CaptureFixture

from funcli.parser import parse_args


def test_parse_args_simple() -> None:
    # Arrange
    def func(a: str, b: int, c: float) -> None: ...

    args = ["--a", "Hello", "--b", "2", "--c", "9.8"]

    # Act & Assert
    pargs = parse_args(inspect.signature(func), args=args)
    assert pargs == {"a": "Hello", "b": 2, "c": 9.8}


def test_parse_args_defaults() -> None:
    # Arrange
    def func(a: str = "Hello", b: int = 22) -> None: ...

    args = ["--a", "Override"]

    # Act & Assert
    pargs = parse_args(inspect.signature(func), args=args)
    assert pargs == {"a": "Override", "b": 22}


def test_parse_args_required(capsys: CaptureFixture[str]) -> None:
    # Arrange
    def func(a: str, b: int = 9000) -> None: ...

    args = ["--b", "8000"]

    # Act & Assert
    with pytest.raises(SystemExit) as einfo:
        parse_args(inspect.signature(func), args=args)

    assert einfo.value.code == 2

    stdout, stderr = capsys.readouterr()
    assert "the following arguments are required: --a" in stderr


@pytest.mark.parametrize(
    "args, vars",
    [
        (["--names", "Thor", "Odin"], {"names": ("Thor", "Odin")}),
        (["--names", "Thor", "--names", "Odin"], {"names": ("Thor", "Odin")}),
    ],
)
def test_parse_args_tuple(args: Sequence[str], vars: dict[str, Any]) -> None:
    # Arrange
    def func(names: tuple[str, ...]) -> None: ...

    # Act & Assert
    pargs = parse_args(inspect.signature(func), args=args)
    assert pargs == vars
