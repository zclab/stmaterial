# Changing CSS variables

Stmaterial allows customising some css variables. These can be declared directly in [html_theme_options](https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_theme_options), in your `conf.py`.

## changing sidenav width

Stmaterial allows defining CSS variables that overrides its default values. The exact variable names to use can be found in Stmaterial’s source code.

You can specifying `sidenav-width` to change the width of sidenav using the following configuration,

```py
html_theme_options = {
    "css_variables": {
        "sidenav-width": "320px",
    },
}
```

## changing colors

You can change the colors of the theme by specifying corresponding variables, for example:

```py
html_theme_options = {
    "css_variables": {
        "primary-color": "#3949ab",
        "primary-color-dark": "#283593",
        "primary-color-raised-hover-solid": "#5c6bc0",
        "primary-color-raised-focus-solid": "#5c6bc0",
    },
}
```
