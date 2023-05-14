# Header configuration

## Fix navbar header

The navbar header will be hidded when scrolling, to make navbar header fixed when scrolling, using the following configuration,

```python
html_theme_options = {
    "fix_header_nav": True,
}
```

## Changing header icons

Stmaterial allows customising the icons that are presented in the header. These icons can be used to link to relevant resources for your project and documentation. To add custom header icons, you need to provide the `header_icons` configuration value to Stmaterial.

```python
html_theme_options = {
    "header_icons": [
        {"name":"Github", "url": "http://github.com/zclab/stmaterial", "svg":"github.svg"},
        {"name":"Gitlab", "url": "http://gitlabcom/zclab/stmaterial", "fontawesome":"fa-brands fa-gitlab"},
    ],
}
```

````{note}
If you wish to use Font Awesome icons in the header, Using `html_css_files` to add the CSS file(s) for Font Awesome.
```python
html_css_files = [
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/fontawesome.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/solid.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/brands.min.css",
]
```
````
