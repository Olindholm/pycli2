import sys
from collections.abc import Callable, Sequence
from inspect import signature
from typing import TypeVar

from ._parser import parse_args

R = TypeVar("R")


def main(
    prog: str,
    func: Callable[..., R],
) -> R:
    return _main(func, sys.argv[1:], prog)


def _main(
    func: Callable[..., R],
    args: Sequence[str],
    prog: str | None = None,
) -> R:
    return func(
        **parse_args(
            signature(func),
            args,
            prog,
        )
    )


__all__ = ["main", "_main"]
