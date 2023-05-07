# Changing fonts

Stmaterial makes it fairly straightforward to change the fonts across the entire page. Using the following theme options to change the font:

```py
html_theme_options = {
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
```


