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

[sphinx-file-wide-metadata]: https://www.sphinx-doc.org/en/master/usage/restructuredtext/field-lists.html#metadata
