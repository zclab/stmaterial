# Page Table of Contents

## Hiding Table of Contents

Stmaterial supports hiding the Table of Contents. To explicitly hide it on a specific page, `hide-toc` can be set in the [File-Wide metadata][sphinx-file-wide-metadata] for that page. See [Page example with hidding table of contents](../examples/pages/hidetoc.md).

````{tab} reStructuredText
```rst
:hide-toc:

[page contents]
```
````

````{tab} Markdown (MyST)
```yaml
---
hide-toc: true
---

[page contents]
```
````

## Hiding Table of Contents navigation

Stmaterial supports hiding the Table of Contents navigation. To explicitly hide it on a specific page, `hide-tocnav` can be set in the [File-Wide metadata][sphinx-file-wide-metadata] for that page. See [Page example with hidding table of contents navigation](../examples/pages/hidetocnav.md).

````{tab} reStructuredText
```rst
:hide-tocnav:

[page contents]
```
````

````{tab} Markdown (MyST)
```yaml
---
hide-tocnav: true
---

[page contents]
```
````

## Enable full width of a page

Stmaterial supports enable full width of a page (hidding sidenav and tocnav). To explicitly enable full width on a specific page, `full-width` can be set in the [File-Wide metadata][sphinx-file-wide-metadata] for that page. See [Page example with full width ](../examples/pages/fullwidth.md).

````{tab} reStructuredText
```rst
:full-width:

[page contents]
```
````

````{tab} Markdown (MyST)
```yaml
---
full-width: true
---

[page contents]
```
````

[sphinx-file-wide-metadata]: https://www.sphinx-doc.org/en/master/usage/restructuredtext/field-lists.html#metadata
