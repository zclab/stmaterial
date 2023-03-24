project = "Simple Sphinx Doc"
copyright = "2023"
author = "zclab"
master_doc = "index"
version = "0.0.3"
language = 'zh_CN'

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "stmaterial.demo.sphinxext",
    "myst_parser",
    "sphinx_inline_tabs",
]


myst_enable_extensions = ["colon_fence", "deflist"]
exclude_patterns = [
    "_build", 
    "Thumbs.db", 
    ".DS_Store",
    "contributing"
]



templates_path = ["_templates"]
html_static_path = ["_static"]
html_theme = "stmaterial"
html_title = "Simple Sphinx Doc"
html_favicon = "_static/favicon.png"
html_last_updated_fmt = ""
html_logo = "_static/logo.png"

todo_include_todos = True


html_theme_options = {
    "source_repository": "http://github.com/zclab/stmaterial",
    "logo":{
        "text": "Logo",
        "logo": "_static/logo.png"
    },
    "external_links": {},
    "show_toc_level": 1,
    "navbar_style": "breadcrumbs", # options: None, breadcrumbs, navigation,
    "header_icons": [
        {"name":"Github", "url": "http://github.com/zclab/stmaterial", "class":"fa-brands fa-github"},
        {"name":"Gitlab", "url": "http://github.com/zclab/stmaterial", "class":"fa-brands fa-gitlab"},
    ],
    "use_edit_page_button": True
}
    
