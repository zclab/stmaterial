# Source Buttons

Source buttons are links to the source of your page’s content (either on your site, or on hosting sites like GitHub).

## Add an edit button

You can add a button to each page that will allow users to edit the page text directly and submit a pull request to update the documentation. To add an edit button, use the following configuration:

```py
html_theme_options = {
    "use_edit_page_button": True
}
```

By default, an edit buttion is added at the bottom of a page. You can also place the edit button at the top of a page using the following configuration:

```py
html_theme_options = {
    "article_top_right": "edit-this-page.html"
}
```

### With popular VCS hosts

Provide the relevant VCS variables, by setting the following keys in [html_theme_options](https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_theme_options):

```py
html_theme_options = {
    "source_repository": "https://github.com/zclab/stmaterial/",
    "source_branch": "main",
    "source_directory": "docs/",
}
```

### With arbitrary URLs

Use arbitrary URLs for the edit button, by setting the following key in [html_theme_options](https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_theme_options):

```py
html_theme_options = {
    "source_edit_link": "https://my.awesome.host.example.com/awesome/project/edit/{filename}",
}
```

The `{filename}` component will be replaced with the full path to the file, as known from the base of the documentation directory.

## View Source link

By default, this theme adds a button link to view the source of a page at the top of the page. To disable it, use the following configuration:

```py
html_show_sourcelink = False
```

You can also place the source link button at the bottom of a page using the following configuration:

```py
html_theme_options = {
    "article_bottom_right": "sourcelink.html"
}
```
