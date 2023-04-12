# Images

Images can be a great supplement to technical documentation text. Sphinx provides control for their alignment in the content, as well as the ability to add captions.

## Basic Usage

```{stm-demo}
![](https://source.unsplash.com/200x200/daily?cute+animals)

This is from Markdown.

+++

.. image:: https://source.unsplash.com/200x200/daily?cute+animals

This is from reStructuredText.
```

## Alignment

````{stm-demo}
```{image} https://source.unsplash.com/200x200/daily?cute+animals
:align: center
```

This is from Markdown.

+++

.. image:: https://source.unsplash.com/200x200/daily?cute+animals
   :align: center


This is from reStructuredText.
````

## Captions

````{stm-demo}

```{figure} https://source.unsplash.com/200x200/daily?cute+animals
This is a captioned image, which needs the "figure" directive.
```

This is from Markdown.

+++

.. figure:: https://source.unsplash.com/200x200/daily?cute+animals

    This is a captioned image, which needs the "figure" directive.

This is from reStructuredText.
````
