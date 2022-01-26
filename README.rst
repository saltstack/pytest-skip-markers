.. image:: https://img.shields.io/github/workflow/status/saltstack/pytest-skip-markers/CI?style=plastic
   :target: https://github.com/saltstack/pytest-skip-markers/actions/workflows/testing.yml
   :alt: CI


.. image:: https://readthedocs.org/projects/pytest-skip-markers/badge/?style=plastic
   :target: https://pytest-skip-markers.readthedocs.io
   :alt: Docs


.. image:: https://img.shields.io/codecov/c/github/saltstack/pytest-skip-markers?style=plastic&token=CqV7t0yKTb
   :target: https://codecov.io/gh/saltstack/pytest-skip-markers
   :alt: Codecov


.. image:: https://img.shields.io/pypi/pyversions/pytest-skip-markers?style=plastic
   :target: https://pypi.org/project/pytest-skip-markers
   :alt: Python Versions


.. image:: https://img.shields.io/pypi/wheel/pytest-skip-markers?style=plastic
   :target: https://pypi.org/project/pytest-skip-markers
   :alt: Python Wheel


.. image:: https://img.shields.io/badge/code%20style-black-000000.svg?style=plastic
   :target: https://github.com/psf/black
   :alt: Code Style: black


.. image:: https://img.shields.io/pypi/l/pytest-skip-markers?style=plastic
   :alt: PyPI - License


..
   include-starts-here

====================
What is Skip Markers
====================

This pytest plugin was extracted from `pytest-salt-factories`_. It's a collection of
of useful skip markers created to simplify and reduce code required to skip tests in
some common scenarios, for example, platform specific tests.

.. _pytest-salt-factories: https://github.com/saltstack/pytest-salt-factories


Install
=======

Installing Skip Markers is as simple as:

.. code-block:: bash

   python -m pip install pytest-skip-markers


And, that's honestly it.


Usage
=====

Once installed, you can now skip some tests with some simple pytest markers, for example.

.. code-block:: python

   import pytest


   @pytest.mark.skip_unless_on_linux
   def test_on_linux():
       assert True


Contributing
============

The pytest-skip-markers project team welcomes contributions from the community.
For more detailed information, refer to `CONTRIBUTING`_.

.. _CONTRIBUTING: https://github.com/saltstack/pytest-skip-markers/blob/main/CONTRIBUTING.md

..
   include-ends-here

Documentation
=============

The full documentation can be seen `here <https://pytest-skip-markers.readthedocs.io>`_.
