===============================
Sambuca
===============================

* Free software: ??? license

Installation
============

::

    pip install sambuca

Documentation
=============
**To Do: insert link to documentation**

Development
===========

To run the all tests run::

    py.test

To generate a Stash compatible README.md file from an rst file, use pandoc
prior to a Git commit. The CONTRIBUTING.rst file is probably most appropriate
during the pre-release phase of development::

    module load pandoc
    pandoc -o README.md CONTRIBUTING.rst
