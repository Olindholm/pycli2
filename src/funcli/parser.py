from argparse import ArgumentParser
from collections.abc import Sequence
from inspect import Parameter, Signature
from typing import Any, Literal, cast, get_args, get_origin

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
        action, nargs = _get_action_nargs(annotation)
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


def _get_action_nargs(
    annotation: Any,
) -> tuple[Literal["extend"], Literal["+"]] | tuple[None, None]:
    outertype, innertypes = _get_types(annotation)

    if issubclass(outertype, Sequence) and not issubclass(outertype, str):
        return "extend", "+"

    return None, None


def _get_types(annotation: type) -> tuple[type, tuple[type, ...]]:
    if type(annotation) is type:
        return annotation, tuple()

    outertype, innertype = get_origin(annotation), get_args(annotation)
    return cast(type, outertype), innertype


def _validate_type(value: Any, annotation: type) -> Any:
    return TypeAdapter(annotation).validate_python(value)
