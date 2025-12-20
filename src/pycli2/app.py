from collections.abc import Sequence

from ._parser import Func, R, parse_func_args


def run(
    *callables: Func[R],
    args: Sequence[str] | None = None,
    prog: str | None = None,
    description: str | None = None,
    epilog: str | None = None,
) -> R:
    """Runs a CLI program with the callables as run options.

    Args:
        callables: Callable functions possible to run (choose) from CLI.
        args: The CLI arguments to parse, or sys.argv if None.
        prog: The name of the program.
        description: The description of the program, shown when using help flags.
        epilog: The program epilog (bottom of the program description).
    """
    func, kwargs = parse_func_args(
        *callables,
        args=args,
        prog=prog,
        description=description,
        epilog=epilog,
    )
    return func(**kwargs)
