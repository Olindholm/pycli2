Get Started
===========

This package simplfies the creation of CLI apps, by analysing the typing of python functions and
parsing command line arguments.


Installation
------------

The python package, both wheel and source distribution is available at `PyPI pycli2 project`_.
Install using your python package manager of choice. E.g. `pip`_ or `uv`_

.. _PyPI pycli2 project: https://pypi.org/project/pycli2/
.. _pip: https://pip.pypa.io/en/stable/installation/
.. _uv: https://docs.astral.sh/uv/

.. code-block:: console

   $ uv pip install lumache


Usage
-----

The package comes with a demo CLI, which the source of is:

.. literalinclude:: ../src/pycli2/__main__.py


It can be accessed by running

.. code-block:: console

   $ python -m pycli --help

In order to make your own CLI, simply import :code:`pycli2` and use the :code:`pycli2.run` function.
Provide it with functions, and it'll automatically create a CLI app from the function typing and
function docstring.

.. code-block:: python

    import pycli2

    if __name__ == "__main__":
        # This will expose firstfunc, secondfunc, and thirdfunc to the CLI.
        pycli2.run(
            firstfunc,
            secondfunc,
            thirdfunc,
        )
