# PyCLI2

Python library to auto parse command line args from function typing.

# Overview

This package simplfies the creation of CLI apps, by analysing the typing of python functions and
parsing command line arguments.

# Installation

The python package, both wheel and source distribution is available at
[PyPI pycli2 project](https://pypi.org/project/pycli2/). Install using your python package manager
of choice. E.g. pip.
```sh
pip install pycli2
```

# Usage

The package comes with a demo CLI, which the source can be view at
[src/pycli2/\_\_main\_\_.py](src/pycli2/__main__.py). It can be accessed by running
```sh
python -m pycli --help
```

In order to make your own CLI, simply import `pycli2` and use the `pycli2.run` function.
Provide it with functions, and it'll automatically create a CLI app from the function
typing and function docstring.

```python
import pycli2

if __name__ == "__main__":
    # This will expose firstfunc, secondfunc, and thirdfunc to the CLI.
    pycli2.run(
        firstfunc,
        secondfunc,
        thirdfunc,
    )
```

# Contributing

...

# License

This project is licensed under the [GNU General Public License v3.0 only](LICENSE.md).
