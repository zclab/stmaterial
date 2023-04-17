import sys
from os.path import abspath, join, dirname
sys.path.insert(0, abspath(join(dirname(__file__), "../src")))
import stmaterial


project = "sphinx theme of material"
copyright = "2023"
author = "zclab"
master_doc = "index"
version = stmaterial.__version__
language = 'en'

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "stmaterial.demo.sphinxext",
    "myst_parser",
    "sphinx_inline_tabs",
    "ablog",
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
html_title = "sphinx theme of material"
html_favicon = "_static/favicon.png"
html_last_updated_fmt = ""
html_logo = "_static/logo.png"

todo_include_todos = True


html_theme_options = {
    "header_links_before_dropdown": 5,
    "source_repository": "https://github.com/zclab/stmaterial",
    "source_branch": "main",
    "source_directory": "docs/",
    "show_back_to_top": True,
    "fix_header_nav": False,
    "logo":{
        "text": "Logo",
        "logo": "_static/logo.png"
    },
    "external_links": [
        {"name": "Furo", "url": "https://pradyunsg.me/furo/quickstart/"},
        {"name": "Sphinx book theme", "url": "https://sphinx-book-theme.readthedocs.io/en/latest/"},
        {"name": "Pydata sphinx theme", "url": "https://pydata-sphinx-theme.readthedocs.io/"},
    ],
    "show_toc_level": 1,
    "header_icons": [
        {"name":"Github", "url": "http://github.com/zclab/stmaterial", "svg":"github.svg"},
        {"name":"Email", "url": "example@example.com", "material_icons":"email"},
    ],
    "use_edit_page_button": True,
    "custom_fonts": {
        "name": 'LXGWWenKaiLite',
        "type": 'truetype',
        "src": [
            {"weight": 200, "url":"https://cdn.jsdelivr.net/gh/zclab/static/fonts/LxgwWenKai-Lite/LXGWWenKaiLite-Light.ttf"},
            {"weight": 300, "url":"https://cdn.jsdelivr.net/gh/zclab/static/fonts/LxgwWenKai-Lite/LXGWWenKaiLite-Light.ttf"},
            {"weight": 400, "url":"https://cdn.jsdelivr.net/gh/zclab/static/fonts/LxgwWenKai-Lite/LXGWWenKaiLite-Regular.ttf"},
            {"weight": 500, "url":"https://cdn.jsdelivr.net/gh/zclab/static/fonts/LxgwWenKai-Lite/LXGWWenKaiLite-Bold.ttf"},
            {"weight": 600, "url":"https://cdn.jsdelivr.net/gh/zclab/static/fonts/LxgwWenKai-Lite/LXGWWenKaiLite-Bold.ttf"},
        ],
    },
}
    

blog_path = "blog"
blog_post_pattern = "posts/*/*"
blog_authors = {
    "zclab": ("子川", "https://github.com/zclab"),
}

# https://github.com/hung1001/font-awesome-pro-v6
fontawesome_link_cdn = "https://cdn.staticaly.com/gh/hung1001/font-awesome-pro-v6/44659d9/css/all.min.css"
fontawesome_included = True

html_sidebars = {
    "posts/**": [
        "sidebar/brand.html", "sidebar/search.html", "ablog/postcard.html","ablog/categories.html","ablog/tagcloud.html", "ablog/recentposts.html",
    ],
    "blog": [
        "sidebar/brand.html", "sidebar/search.html", "ablog/categories.html","ablog/tagcloud.html","ablog/archives.html","ablog/recentposts.html",
    ],
    "blog/**": [
        "sidebar/brand.html", "sidebar/search.html", "ablog/categories.html","ablog/tagcloud.html","ablog/archives.html","ablog/recentposts.html",
    ],
}