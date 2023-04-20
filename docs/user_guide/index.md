# User Guide

This section serves to guide the user with customising stmaterial-based documentation. This page lists all the theme-specific customisations, as provided by this theme. Other pages in this section provide guidance for making specific customisations when using Sphinx with stmaterial.

```{toctree}
:hidden:

quickstart
logo
edit-button
fonts
header
landing-page
sidebar
sidebar-title
toc
```

## Theme options

[`html_theme_options`][sphinx-html_theme_options] in `conf.py` is used for customisations that affect the entire documentation. This is for stuff like fonts and colors.

```{note}
Note that only the configuration options listed here are supported (not the ones inherited from the built-in `basic` Sphinx theme).
```

(css-variables)=

### `light_css_variables`/`dark_css_variables`

Stmaterial makes extensive use of [CSS variables][css-variables]. These can be overridden by the user and are used for stylizing nearly all elements of the documentation. 

Setting `*_css_variables` is the recommended mechanism to override Stmaterial's default values for these variables.

```python
html_theme_options = {
    "light_css_variables": {
        "color-brand-primary": "red",
        "color-brand-content": "#CC3333",
        "color-admonition-background": "orange",
    },
}
```

```{caution}
Typos in the `*_css_variables` dictionary are silently ignored, and do not raise any errors or warnings. Double check that your spellings and values are correct and valid.
```

(top_of_page_button)=

### `use_edit_page_button`

Controls whether to show edit this page button, default is `False`.

```python
html_theme_options = {
    "use_edit_page_button": True,
}
```

### `header_icons`

Changes the icons presented in the site header. See {doc}`./header` for the details.

## Page specific tweaks

[File-Wide metadata][sphinx-file-wide-metadata] is used for per-page customisation, primarily for controlling which UI elements are presented.

### `hide-toc`

The “Contents” sidebar is automatically hidden for any pages that don’t have any inner headings. It is possible to hide it even when a page has inner headings, by setting `hide-toc` at the page level. See {doc}`./toc` for an example.


[css-variables]: https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties
[sphinx-html_theme_options]: https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_theme_options
[sphinx-file-wide-metadata]: https://www.sphinx-doc.org/en/master/usage/restructuredtext/field-lists.html#metadata
