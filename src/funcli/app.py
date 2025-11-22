from collections.abc import Sequence

from ._parser import Func, R, parse_func_args


def run(
    *callables: Func[R],
    args: Sequence[str] | None = None,
    prog: str | None = None,
    description: str | None = None,
    epilog: str | None = None,
) -> R:
    func, kwargs = parse_func_args(
        *callables,
        args=args,
        prog=prog,
        description=description,
        epilog=epilog,
    )
    return func(**kwargs)
