---
hide-toc: true
hide-sidenav: true
---


# A Materialize based sphinx theme

This is a materialize based sphinx theme, see the [materialize documentation](https://materializeweb.com/) for reference. 

```{gallery-grid}
:grid-columns: 1 2 2 3

- header: "{fab}`bootstrap;pst-color-primary` Built with Bootstrap"
  content: "Use Bootstrap classes and functionality in your documentation."
- header: "{fas}`bolt;pst-color-primary` Responsive Design"
  content: "Site sections will change behavior and size at different screen sizes."
- header: "{fas}`circle-half-stroke;pst-color-primary` Light / Dark theme"
  content: "Users can toggle between light and dark themes interactively."
- header: "{fas}`palette;pst-color-primary` Customizable UI and themes"
  content: "Customize colors and branding with CSS variables, and build custom UIs with [Sphinx Design](user_guide/web-components)."
- header: "{fab}`python;pst-color-primary` Supports PyData and Jupyter"
  content: "CSS and UI support for Jupyter extensions and PyData execution outputs."
  link: "examples/pydata.html"
- header: "{fas}`lightbulb;pst-color-primary` Example Gallery"
  content: "See our gallery of projects that use this theme."
  link: "examples/gallery.html"
```

```{toctree}
:maxdepth: 2

user_guide/index
```

```{toctree}
:maxdepth: 2

examples/index
```

```{toctree}
:caption: Demo
:maxdepth: 2

Components <web-components>
```

```{toctree}
:hidden:

blog
```

```{toctree}
:caption: Development
:hidden:

Develop <develop>
```
