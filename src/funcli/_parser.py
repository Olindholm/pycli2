from argparse import ArgumentParser
from collections.abc import Iterable, Mapping, Sequence
from inspect import Parameter, Signature
from types import GenericAlias, NoneType, UnionType
from typing import Any, cast, get_args, get_origin

from pydantic import TypeAdapter


def parse_args(
    sig: Signature,
    args: Sequence[str],
    prog: str | None = None,
) -> dict[str, Any]:
    parser = ArgumentParser(
        prog=prog,
        description="What the program does",
        epilog="Text at the bottom of help",
    )

    for name, param in sig.parameters.items():
        annotation: type = param.annotation
        action, nargs = get_argtype(get_types(annotation))
        required = param.default == Parameter.empty
        metavar = type(annotation).__name__ + ("" if required else f" (default: {param.default})")

        parser.add_argument(
            f"--{name.replace('_', '-')}",
            action=action,  # type: ignore
            nargs=nargs,
            default=None if required else param.default,
            required=required,
            metavar=metavar,
        )

    kwargs = vars(parser.parse_args(args))
    return {
        key: _validate_type(value, sig.parameters[key].annotation) for key, value in kwargs.items()
    }


ArgType = tuple[str | None, int | str | None]


def get_argtype(types: Iterable[type]) -> ArgType:
    nullable = NoneType in types
    if nullable:
        types = set(types)
        types.discard(NoneType)

    if all(is_listlike(type_) for type_ in types):
        return "extend", "+"
    if all(is_dictlike(type_) for type_ in types):
        return "extend", "+"

    if any(is_listlike(type_) or is_dictlike(type_) for type_ in types):
        raise TypeError()

    return None, None


def is_listlike(type_: type) -> bool:
    return issubclass(type_, Sequence) and not issubclass(type_, str) or issubclass(type_, set)


def is_dictlike(type_: type) -> bool:
    return issubclass(type_, Mapping)


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
