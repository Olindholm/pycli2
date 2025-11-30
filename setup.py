import os
import subprocess
from collections.abc import Sequence
from distutils.util import strtobool
from email.parser import Parser
from pathlib import Path
from typing import NoReturn

from semver import Version
from setuptools import setup


def get_version() -> Version:
    return get_pkg_info_version() or get_git_version() or raise_version_error()


def get_pkg_info_version(pkg_info_file: Path = Path("PKG-INFO")) -> Version | None:
    if not pkg_info_file.exists():
        return None

    with pkg_info_file.open() as f:
        data = Parser().parse(f)

    try:
        return Version.parse(data["Version"])
    except KeyError:
        return None


def get_git_version(version_file: Path = Path("version.txt")) -> Version | None:
    if not version_file.exists():
        return None

    base = version_file.read_text().strip()
    suffix = get_git_count_commits(version_file)
    build = os.environ.get("BUILD", "dev")

    return Version.parse(f"{base}.{suffix}" + (f"+{build}" if build else ""))


def get_git_count_commits(file: Path) -> int:
    shallow, _ = sh(("git", "rev-parse", "--is-shallow-repository"))
    if strtobool(shallow):
        raise RuntimeError("Git repository is shallow!")

    vcommit, _ = sh(("git", "log", "--first-parent", "-1", "--pretty=%H", "--", file.as_posix()))
    count, _ = sh(("git", "rev-list", "--first-parent", "--count", f"{vcommit}..HEAD"))
    return int(count)


def sh(args: Sequence[str]) -> tuple[str, str]:
    process = subprocess.run(args, capture_output=True, check=True)
    return process.stdout.decode().strip(), process.stderr.decode().strip()


def raise_version_error() -> NoReturn:
    raise RuntimeError("Could not determine version!")


setup(version=str(get_version()))
