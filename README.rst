
.. image:: https://github.com/allekmott/aamras/workflows/build/badge.svg
    :target: https://github.com/allekmott/aamras/workflows/build/badge.svg
    :alt: build status

.. image:: https://readthedocs.org/projects/aamras/badge/?version=latest
    :target: https://aamras.readthedocs.io/en/latest/?badge=latest
    :alt: documentation status

.. image:: https://img.shields.io/pypi/pyversions/aamras.svg
    :target: https://pypi.python.org/pypi/aamras
    :alt: supported python versions

**aam ras** or *आम रस* - Hindi for mango juice 🥭.

It is pronounced "*arm Russ*" if the *r* in *arm* is silent.

aamras provides a high-level interface for headless browser manipulation.
It is currently built on `selenium <https://github.com/SeleniumHQ/selenium>`_.

Requirements
------------
*aamras* requires Python 3.6 or above.

Installation
------------
The base *aamras* package may be installed using pip:

.. code-block::

    pip install aamras

Additional drivers (webdrivers) are also required for the actual browser manipulation side of things. The
`webdrivermanager CLI tool <https://github.com/rasjani/webdrivermanager>`_ can streamline the installation
process, but otherwise, there's always the core documentation for the drivers:

- For Firefox - `geckodriver <https://firefox-source-docs.mozilla.org/testing/geckodriver/>`_
- For Chrome - `chromedriver <https://sites.google.com/a/chromium.org/chromedriver/getting-started>`_
