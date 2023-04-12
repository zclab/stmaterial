<h1 align="center">
  <img src="docs/_static/logo.png" width="400">
</h1>

[![deploy](https://github.com/zclab/stmaterial/actions/workflows/deploy-docs.yml/badge.svg)](https://zclab.github.io/stmaterial/)
[![release](https://img.shields.io/github/release/zclab/stmaterial.svg)](https://github.com/zclab/stmaterial/releases)


A Materialize based sphinx theme


## Installation and usage

To use this theme in the repository, follow these steps:

- Install the `stmaterial` in your doc build environment::

  ```
  pip install -i https://test.pypi.org/simple/ stmaterial
  ```
- Configure the Sphinx docs to use the theme by editing `conf.py`

  ```python
  html_theme = "stmaterial"
  ```
