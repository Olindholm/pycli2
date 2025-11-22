from collections.abc import Sequence
from pathlib import Path
from typing import Any

import pytest
from pydantic import AnyUrl
from pytest import CaptureFixture

from pycli2._parser import parse_func_args


def test_simple() -> None:
    # Arrange
    def func(a: str, b: int, c: float) -> None: ...

    args = ["--a", "Hello", "--b", "2", "--c", "9.8"]

    # Act & Assert
    assert parse_func_args(func, args=["func", *args]) == (func, {"a": "Hello", "b": 2, "c": 9.8})


@pytest.mark.parametrize(
    "args, vars",
    [
        (["--loc", "https://eg.com/file.txt"], {"loc": AnyUrl("https://eg.com/file.txt")}),
        (["--loc", "file.txt"], {"loc": Path("file.txt")}),
        (["--loc", "/root/file.txt"], {"loc": Path("/root/file.txt")}),
        (["--loc", "../file.txt"], {"loc": Path("../file.txt")}),
    ],
)
def test_union(args: Sequence[str], vars: dict[str, Any]) -> None:
    # Arrange
    def func(loc: AnyUrl | Path) -> None: ...

    # Act & Assert
    assert parse_func_args(func, args=["func", *args]) == (func, vars)


def test_defaults() -> None:
    # Arrange
    def func(a: str = "Hello", b: int = 22) -> None: ...

    args = ["--a", "Override"]

    # Act & Assert
    assert parse_func_args(func, args=["func", *args]) == (func, {"a": "Override", "b": 22})


def test_required(capsys: CaptureFixture[str]) -> None:
    # Arrange
    def func(a: str, b: int = 9000) -> None: ...

    args = ["--b", "8000"]

    # Act & Assert
    with pytest.raises(SystemExit) as einfo:
        parse_func_args(func, args=["func", *args])

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
    assert parse_func_args(func, args=["func", *args]) == (func, vars)


@pytest.mark.parametrize(
    "args, vars",
    [
        ([], {"names": None}),
        (["--names", "Thor", "Odin"], {"names": ("Thor", "Odin")}),
        (["--names", "Thor", "--names", "Odin"], {"names": ("Thor", "Odin")}),
    ],
)
def test_parse_args_tuple_none(args: Sequence[str], vars: dict[str, Any]) -> None:
    # Arrange
    def func(names: tuple[str, ...] | None = None) -> None: ...

    # Act & Assert
    assert parse_func_args(func, args=["func", *args]) == (func, vars)


@pytest.mark.parametrize(
    "args, vars",
    [
        (["--names", "Thor", "Odin"], {"names": ["Thor", "Odin"]}),
        (["--names", "Thor", "--names", "Odin"], {"names": ["Thor", "Odin"]}),
    ],
)
def test_list(args: Sequence[str], vars: dict[str, Any]) -> None:
    # Arrange
    def func(names: list[str]) -> None: ...

    # Act & Assert
    assert parse_func_args(func, args=["func", *args]) == (func, vars)


@pytest.mark.parametrize(
    "args, vars",
    [
        ([], {"names": None}),
        (["--names", "Thor", "Odin"], {"names": ["Thor", "Odin"]}),
        (["--names", "Thor", "--names", "Odin"], {"names": ["Thor", "Odin"]}),
    ],
)
def test_list_none(args: Sequence[str], vars: dict[str, Any]) -> None:
    # Arrange
    def func(names: list[str] | None = None) -> None: ...

    # Act & Assert
    assert parse_func_args(func, args=["func", *args]) == (func, vars)


@pytest.mark.parametrize(
    "args, vars",
    [
        (["--names", "Thor", "Odin"], {"names": {"Thor", "Odin"}}),
        (["--names", "Thor", "--names", "Odin"], {"names": {"Thor", "Odin"}}),
    ],
)
def test_set(args: Sequence[str], vars: dict[str, Any]) -> None:
    # Arrange
    def func(names: set[str]) -> None: ...

    # Act & Assert
    assert parse_func_args(func, args=["func", *args]) == (func, vars)


@pytest.mark.parametrize(
    "args, vars",
    [
        ([], {"names": None}),
        (["--names", "Thor", "Odin"], {"names": {"Thor", "Odin"}}),
        (["--names", "Thor", "--names", "Odin"], {"names": {"Thor", "Odin"}}),
    ],
)
def test_set_none(args: Sequence[str], vars: dict[str, Any]) -> None:
    # Arrange
    def func(names: set[str] | None = None) -> None: ...

    # Act & Assert
    assert parse_func_args(func, args=["func", *args]) == (func, vars)


@pytest.mark.parametrize(
    "args, vars",
    [
        (
            ["--genders", "Thor=Male", "Freja=Female"],
            {"genders": {"Thor": "Male", "Freja": "Female"}},
        ),
        (
            ["--genders", "Thor=Male", "--genders", "Freja=Female"],
            {"genders": {"Thor": "Male", "Freja": "Female"}},
        ),
    ],
)
def test_dict(args: Sequence[str], vars: dict[str, Any]) -> None:
    # Arrange
    def func(genders: dict[str, str]) -> None: ...

    # Act & Assert
    assert parse_func_args(func, args=["func", *args]) == (func, vars)


@pytest.mark.parametrize(
    "args, vars",
    [
        ([], {"genders": None}),
        (
            ["--genders", "Thor=Male", "Freja=Female"],
            {"genders": {"Thor": "Male", "Freja": "Female"}},
        ),
        (
            ["--genders", "Thor=Male", "--genders", "Freja=Female"],
            {"genders": {"Thor": "Male", "Freja": "Female"}},
        ),
    ],
)
def test_dict_none(args: Sequence[str], vars: dict[str, Any]) -> None:
    # Arrange
    def func(genders: dict[str, str] | None = None) -> None: ...

    # Act & Assert
    assert parse_func_args(func, args=["func", *args]) == (func, vars)
