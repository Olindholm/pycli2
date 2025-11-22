import logging
import sys
from argparse import Action, ArgumentParser, Namespace
from collections.abc import Callable, Iterable, Mapping, Sequence
from inspect import Parameter, Signature, signature
from types import GenericAlias, NoneType, UnionType
from typing import Any, TypeVar, cast, get_args, get_origin

from pydantic import TypeAdapter
from typing_extensions import override

R = TypeVar("R")
Func = Callable[..., R]

FUNC_DEST = "__FUNC__"
BANNED_KEYWORDS = (FUNC_DEST,)


def parse_func_args(
    *callables: Func[R],
    args: Sequence[str] | None,
    prog: str | None = None,
    description: str | None = None,
    epilog: str | None = None,
) -> tuple[Func[R], dict[str, Any]]:
    if args is None:
        args = sys.argv[1:]

    rootparser = ArgumentParser(
        prog=prog,
        description=description,
        epilog=epilog,
    )
    subparser = rootparser.add_subparsers(
        title="Function to run",
        description="Run the selected function by entering it's name.",
        help="For more function specific info, select it and add -h/--help after it.",
        dest=FUNC_DEST,
        required=True,
        metavar="FUNC",
    )

    funcs = _format_funcs(*callables)
    for name, (func, sig) in funcs.items():
        funcparser = subparser.add_parser(
            name,
            description=func.__doc__,
            help=(func.__doc__ or "").split("\n")[0],
        )

        for key, param in sig.parameters.items():
            if key in BANNED_KEYWORDS:
                raise ValueError(f"Function has a banned keyword {key}!")

            annotation: type = param.annotation
            action, nargs = get_argtype(get_types(annotation))
            required = param.default == Parameter.empty
            metavar = str(annotation) + ("" if required else f" (default: {param.default})")

            funcparser.add_argument(
                f"--{key.replace('_', '-')}",
                action=action,  # type: ignore[arg-type] # action can be None!
                nargs=nargs,
                default=None if required else param.default,
                required=required,
                metavar=metavar,
            )

    cliargs = vars(rootparser.parse_args(args))
    name = cliargs.pop(FUNC_DEST)
    func, sig = funcs[name]
    kwargs = {
        key: _validate_type(value, sig.parameters[key].annotation) for key, value in cliargs.items()
    }

    return func, kwargs


def _format_funcs(*callables: Func[R]) -> dict[str, tuple[Func[R], Signature]]:
    funcs: dict[str, tuple[Func[R], Signature]] = {}
    for callable in callables:
        name = callable.__name__

        if name in funcs:
            raise ValueError(f"Cannot have the same function name ({name}) twice!")

        funcs[name] = callable, signature(callable)

    return funcs


ArgType = tuple[str | type[Action] | None, int | str | None]


def get_argtype(types: Iterable[type]) -> ArgType:
    nullable = NoneType in types
    if nullable:
        types = set(types)
        types.discard(NoneType)

    if all(is_sequenceish(type_) for type_ in types):
        return "extend", "+"
    if all(is_mapish(type_) for type_ in types):
        return MapAction, "+"

    if any(is_sequenceish(type_) or is_mapish(type_) for type_ in types):
        raise TypeError()

    return None, None


def is_sequenceish(type_: type) -> bool:
    """Returns whether the type is sequence(ish).

    Sequence(ish) meaning types such as tuples, lists, sets, etc. Strings are excluded.
    Mappings are technically sequences but are also excluded.
    """
    return issubclass(type_, Sequence) and not issubclass(type_, str) or issubclass(type_, set)


def is_mapish(type_: type) -> bool:
    """Returns whether the type is map(ish).

    Map(ish) meaning basically a map, such as dicts.
    """
    return issubclass(type_, Mapping)


class MapAction(Action):
    def __init__(self, option_strings: str, dest: str, nargs: str | None, **kwargs: Any):
        if nargs is None:
            raise ValueError("nargs must be provided!")

        super().__init__(option_strings, dest, nargs, **kwargs)

    @override
    def __call__(
        self,
        parser: ArgumentParser,
        namespace: Namespace,
        values: Sequence[str],  # type: ignore[override] # This is ensured by __init__
        option_string: str | None = None,
    ) -> None:
        map = getattr(namespace, self.dest) or {}

        for value in values:
            k, v = value.split("=")

            if k in map:
                msg = f"Mapping key {k} was provided more than once. Last value will be used."
                logging.warning(msg)

            map[k] = v

        setattr(namespace, self.dest, map)


def get_types(*annotations: type) -> tuple[type, ...]:
    types: list[type] = []

    for annotation in annotations:
        if type(annotation) is UnionType:
            types.extend(get_types(*get_args(annotation)))

        elif type(annotation) is GenericAlias:
            types.append(cast(type, get_origin(annotation)))

        else:
            types.append(annotation)

    return tuple(types)


def _validate_type(value: Any, annotation: type) -> Any:
    return TypeAdapter(annotation).validate_python(value)
