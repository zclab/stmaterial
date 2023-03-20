---
comment: True
---

# Extra features in this theme

## Extensions

The following extensions are enabled by default: <https://github.com/cessen/str_indices>, <https://gitlab.com/cessen/str_indices>
- [sphinx-copybutton](https://sphinx-copybutton.readthedocs.io/en/latest/)
- [sphinx-togglebutton](https://sphinx-togglebutton.readthedocs.io/en/latest/)
- [sphinx-design2](https://github.com/sphinx-extensions2/sphinx-design2)
- [sphinx-tippy](https://sphinx-tippy.readthedocs.io/en/latest/)
- [sphinx-subfigure](https://sphinx-subfigure.readthedocs.io/en/latest/)

### sphinx subfigure example

````{subfigure} AA|BC
---
layout-sm: A|B|C
gap: 8px
subcaptions: above
name: myfigure
class-grid: outline
---
```{image} /_images/a.png
:height: 100px
:alt: Image A
```
```{image} /_images/b.png
:height: 100px
:alt: Image B
```
```{image} /_images/c.png
:height: 100px
:alt: Image C
```
Figure Caption
````


## strong words

This is a strong words test: **strong**.


## Timeline

:::::{grid} 1 2 3 4
---
gutter: 0
padding: 0
---

::::{grid-item}
---
columns: 12
margin: 0
class: +timeline
---

:::{card}
---
width: 50%
class-card: +entry right sd-rounded-0
---
2022年
^^^^^^^
[sphinx](https://www.sphinx-doc.org/en/master/) (主题使用 [pydata sphinx theme](https://github.com/pydata/pydata-sphinx-theme))
:::

:::{card}
---
width: 50%
class-card: +entry left sd-rounded-0
---
2021年
^^^^^^^^^^^^^^^^^^^^^
[hexo](https://hexo.io/zh-cn/) (使用过 [volantis](https://github.com/volantis-x/hexo-theme-volantis)，[butterfly](https://github.com/jerryc127/hexo-theme-butterfly) 等)
:::

:::{card}
---
width: 50%
class-card: +entry right sd-rounded-0
---
2020年
^^^^^^^^^^^^^^^^^
[typecho](https://github.com/typecho/typecho) (使用过 ``handsome``，[joe](https://github.com/HaoOuBa/Joe) 等)
:::

::::
:::::



## Gallery directive

The following are gallery directive example,

```{gallery-grid} ./_static/links/gallery.yaml
:grid-columns: 1 2 2 4
```


## Giscus comment

Integrated with giscus comment, use `comment: True` meta in page to enable comment for that page. 

```python
html_theme_options = {
    "comment": {
        "enable_blog_comment": True,
        "enable_docs_comment": False,
        "repo": "***/****",
        "repo_id": "************",
        "category": "General",
        "category_id": "*************",
    },
}
```