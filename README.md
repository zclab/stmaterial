<h1 align="center">
  <img src="docs/_static/logo.png" width="400">
</h1>

[![deploy](https://github.com/zclab/stmaterial/actions/workflows/deploy-docs.yml/badge.svg)](https://zclab.github.io/stmaterial/)
[![release](https://img.shields.io/github/release/zclab/stmaterial.svg)](https://github.com/zclab/stmaterial/releases)


A Materialize based sphinx theme


## Installation and usage

To use this theme in the repository, follow these steps:

- Add this theme to the `pip` install requirements of the repo. For now, point it to the `main` branch like so:

  ```
  # in requirements.txt
  git+git@github.com:zclab/stmaterial.git
  ```
- Configure the Sphinx docs to use the theme by editing `conf.py`

  ```python
  html_theme = "stmaterial"
  ```
