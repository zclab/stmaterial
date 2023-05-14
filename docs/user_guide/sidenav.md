# Changing sidenav elements

Stmaterial supports customising the elements that show up in the sidenav (left).

## Default design

The following code snippet lists the fragments (HTML files from Stmaterial's theme folder) that are used for the default sidenav design.

```{literalinclude} ../../src/stmaterial/theme/stmaterial/theme.conf
---
language: ini
start-after: "# sidebar-start"
end-before: "# sidebar-end"
---
```

## Hiding sidenav

Stmaterial supports hiding the sidenav. To explicitly hide it on a specific page, `hide-sidenav` can be set in the [File-Wide metadata][sphinx-file-wide-metadata] for that page..

````{tab} reStructuredText
```rst
:hide-sidenav:

[page contents]
```
````

````{tab} Markdown (MyST)
```yaml
---
hide-sidenav: true
---

[page contents]
```
````

## Set up sidenav icons

Stmaterial allows set up the icons that are presented in the sidenav, there is no sidenav icons by default. To add custom sidenav icons, you need to provide the `sidenav_icons` configuration value to Stmaterial.

```python
html_theme_options = {
    "sidenav_icons": [
        {"name":"Gitlab", "url": "http://gitlabcom/zclab/stmaterial", "fontawesome":"fa-brands fa-gitlab"},
    ],
}
```

[sphinx-file-wide-metadata]: https://www.sphinx-doc.org/en/master/usage/restructuredtext/field-lists.html#metadata
