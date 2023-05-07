# Changing header icons

Stmaterial allows customising the icons that are presented in the header. These icons can be used to link to relevant resources for your project and documentation.


## Default icons

Stmaterial includes [Material Icons](https://marella.me/material-icons/demo/) as default, the use of Material Icons please refer to [Material Icons](https://marella.me/material-icons/demo/).



## Configuration

To add custom header icons, you need to provide the `header_icons` configuration value to Stmaterial. If this configuration value is non-empty, the default header icons are disabled.


```python
html_theme_options = {
    "header_icons": [
        {"name":"Github", "url": "http://github.com/zclab/stmaterial", "svg":"github.svg"},
        {"name":"Email", "url": "example@example.com", "material_icons":"email"},
    ],
}
```

The value for this configuration value is a list of dictionaries. Each dictionary needs to have the following structure:

- `name`: Describes what the destination location is. This is primarily for screen readers.
- `url`: Where clicking on the icon will take users.


### Using icon packs

You can use icon packs that provide icons, with the footer. Usually, icons pack have a non-negligible impact on first page load times and need more data needing to be downloaded. That said, you also get more convenient access to a well designed set of icons. :)

#### Font Awesome

```{note}
With the release of Font Awesome 6, Fonticons Inc has revamped the documentation to consistently upsell their [Kits](https://fontawesome.com/v6/docs/web/setup/use-kit). These kits can help reduce load times on pages but have limited number of page views, so we'll use Font Awesome via a CDN in this example.
```

If you wish to use Font Awesome icons in the footer, it's a two step process.

- Using `html_css_files`, add the CSS file(s) for Font Awesome.

  ```py
  html_css_files = [
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/fontawesome.min.css",
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/solid.min.css",
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/brands.min.css",
  ]
  ```

- Use `class` to use the relevant Font Awesome icons in `footer_icons`. You can search the [free Font Awesome icons](https://fontawesome.com/v6/search?s=solid%2Cbrands), and clicking on a specific icon shows the class you need to use. The configuration would look as follows:

  ```py
  html_theme_options = {
      "footer_icons": [
          {
              "name": "GitHub",
              "url": "https://github.com/zclab/stmaterial",
              "html": "",
              "class": "fa-solid fa-github fa-2x",
          },
      ],
  }
  ```

  Note that the `fa-2x` is necessary to get a reasonable sized icon.


[^1]: Yes, I'm aware that it can be argued that embedding raw HTML in a `conf.py` file is... ugly. :)
[^2]: You need to use your browser's developer tools to get the SVG directly from the page: inspect element + copy svg element (ctrl+c) + paste.
