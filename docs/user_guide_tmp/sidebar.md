# Changing sidebar elements

Stmaterial supports customising the elements that show up in the navigational sidebar (left). This is to provide documentation authors who are willing to work with HTML/CSS to change and tweak how the sidebar looks.

## Expectations

It is expected that users who override the sidebar would also carefully consider how their documentation looks across various platforms (i.e. not take a "looks OK on my machine" approach) and would be willing to override Stmaterial's styles to make it work with their sidebar design.

Some things to consider when doing this are:

- different OSs/browsers handle scrollbars and their widths differently,
  with different effects on the layouting
- end users can customise the look of their default scrollbars at an OS level(like overlay, hidden, visible-and-takes-space and maybe more?)
- different viewport heights will differ across devices
- "user interaction flows", such as looking for a certain page in the sidebar or via search.

## Default design

The following code snippet lists the fragments (HTML files from Stmaterial's theme folder) that are used for the default sidebar design.

```{literalinclude} ../../src/stmaterial/theme/stmaterial/theme.conf
---
language: ini
start-after: "# sidebar-start"
end-before: "# sidebar-end"
---
```

## Making changes

There are two main ways to customise Stmaterial's sidebar:

- override the content of the default templates with your own templates, using [`templates_path`][sphinx-templates_path].
- change the entire sidebar structure, using [`html_sidebars`][sphinx-html_sidebars].

### Using `templates_path`

This is useful when you want to change a specific element of the sidebar. A good example for when you might want to use this: adding a tagline after your project's name/logo.

This is done by setting [`templates_path`][sphinx-templates_path] in the `conf.py` and correctly adding files within the configured paths.

```python
templates_path = ["_templates"]
```

For the above example -- adding a tagline after the name/logo -- you'd want to add an `_templates/sidebar/brand.html` file, that overrides the appropriate content. For more information on how to do so, [Sphinx's templating documentation][templating].

### Using `html_sidebars`

This is useful when you want to make drastic or major changes to the design of Stmaterial's sidebar.

```py
html_sidebars = {
    "**": [
        "sidebar/brand.html", "sidebar/search.html", "sidebar/sidenav.html"
    ]
}
```

[sphinx-templates_path]: https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-templates_path
[sphinx-html_sidebars]: https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_sidebars
[templating]: https://www.sphinx-doc.org/en/master/development/theming.html#templating
