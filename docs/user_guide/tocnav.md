# Page Table of Contents

## Hiding Table of Contents

Stmaterial supports hiding the Table of Contents. To explicitly hide it on a specific page, `hide-toc` can be set in the [File-Wide metadata][sphinx-file-wide-metadata] for that page. See [Hide Table of contents example](../examples/hidetoc.md).

````{tab} reStructuredText
```rst
:hide-toc:

[page contents]
```
````

## Hiding Table of Contents navigation

Stmaterial supports hiding the Table of Contents navigation. To explicitly hide it on a specific page, `hide-tocnav` can be set in the [File-Wide metadata][sphinx-file-wide-metadata] for that page. See [Hiding Table of Contents navigation example](../examples/hidetocnav.md).

````{tab} reStructuredText
```rst
:hide-tocnav:

[page contents]
```
````

[sphinx-file-wide-metadata]: https://www.sphinx-doc.org/en/master/usage/restructuredtext/field-lists.html#metadata
