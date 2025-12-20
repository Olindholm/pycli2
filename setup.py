import os
from email.parser import Parser
from pathlib import Path

from packaging.version import Version
from setuptools import setup


def get_version() -> Version:
    return get_pkg_info_version() or get_env_version() or default_dev_version()


def get_pkg_info_version(pkginfo_file: Path = Path("PKG-INFO")) -> Version | None:
    if not pkginfo_file.exists():
        return None

    with pkginfo_file.open() as f:
        pkginfo = Parser().parse(f)

    try:
        return Version(pkginfo["Version"])
    except KeyError:
        return None


def get_env_version(envname: str = "PACKAGE_VERSION") -> Version | None:
    try:
        return Version(os.environ[envname])
    except KeyError:
        return None


def default_dev_version(vfile: Path = Path("version.txt")) -> Version:
    base = vfile.read_text().strip()
    return Version(f"{base}+dev")


setup(version=str(get_version()))
