========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |appveyor|
        |
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/pset-4-5/badge/?style=flat
    :target: https://readthedocs.org/projects/pset-4-5
    :alt: Documentation Status

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/nhvin118/pset-4-5?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/nhvin118/pset-4-5

.. |version| image:: https://img.shields.io/pypi/v/pset-4.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/pset-4

.. |commits-since| image:: https://img.shields.io/github/commits-since/nhvinh118/pset-4-5/v0.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/nhvinh118/pset-4-5/compare/v0.0.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/pset-4.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/pset-4-5

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/pset-4-5.svg
    :alt: Supported versions
    :target: https://pypi.org/project/pset-4-5

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/pset-4-5.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/pset-4-5


.. end-badges

Pset 4-5

* Free software: MIT license

Installation
============

::

    pip install pset-4-5

Documentation
=============


https://pset-4-5.readthedocs.io/


Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
