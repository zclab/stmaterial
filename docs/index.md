---
hide-toc: true
hide-navigation: true
---


# Sphinx theme of material

A simple sphinx documentation theme based on [Furo](https://pradyunsg.me/furo/quickstart/) with lightweighted modification. A simple sphinx documentation theme based on Furo with lightweighted modification. A simple sphinx documentation theme based on Furo with lightweighted modification.

Cards and tabs provide some extra UI flexibility for your content. Both sphinx-design and sphinx-panels can be used with this theme. This theme provides custom CSS to ensure that their look and feel is consistent with this theme.

This project enables writing documentation with Markdown in Sphinx[1]. This is achieved by making well-thought-out extensions to the CommonMark Specification, which make it as capable as reStructuredText. In case you’re wondering if that works well… this documentation is written using MyST.

Markdown is a significantly more popular markup format than reStructuredText. This means that it’s likely that potential contributors/developers on the project are significantly more familiar with Markdown than reStructuredText. MyST gives you the best of both worlds – simplicity and familiarity of Markdown with the extensibility power of reST.

This project provides a live-reloading server, that rebuilds the documentation and refreshes any open pages automatically when changes are saved. This enables a much shorter feedback loop which can help boost productivity when writing documentation.


```{toctree}
:maxdepth: 2
:hidden:

quickstart
customisation/index
reference/index
recommendations
```

```{toctree}
:caption: Demo
:maxdepth: 2
:hidden:

Features <features>
Develop <develop>
Components <web-components>
```

```{toctree}
:caption: Development
:hidden:

kitchen-sink/index
```
