import hashlib
import logging
import os
from pygments.formatters import HtmlFormatter
from pygments.style import Style
from pygments.token import Text
from sphinx.highlighting import PygmentsBridge
import sphinx.application
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.locale import get_translation
from ._navigation import add_toctree_functions
from ._transforms import ShortenLinkTransform, WrapTableAndMathInAContainerTransform
from .utils import get_theme_options, config_provided_by_user
from .directives import GalleryDirective


__version__ = "0.0.8.dev1"
logger = logging.getLogger(__name__)

MESSAGE_CATALOG_NAME = "stmaterial"
_KNOWN_STYLES_IN_USE: Dict[str, Optional[Style]] = {
    "light": None,
    "dark": None,
}


def update_known_styles_state(app: sphinx.application.Sphinx) -> None:
    """Update a global store of known styles of this application."""
    global _KNOWN_STYLES_IN_USE

    _KNOWN_STYLES_IN_USE = {
        "light": _get_light_style(app),
        "dark": _get_dark_style(app),
    }


def _get_light_style(app: sphinx.application.Sphinx) -> Style:
    return app.builder.highlighter.formatter_args["style"]


def _get_dark_style(app: sphinx.application.Sphinx) -> Style:
    # HACK: begins here
    dark_style = None
    try:
        if (
            hasattr(app.config, "_raw_config")
            and isinstance(app.config._raw_config, dict)
            and "pygments_dark_style" in app.config._raw_config
        ):
            dark_style = app.config._raw_config["pygments_dark_style"]
    except (AttributeError, KeyError) as e:
        logger.warning(
            (
                "ssdoc could not determine the value of `pygments_dark_style`. "
                "Falling back to using the value provided by Sphinx.\n"
                "Caused by %s"
            ),
            e,
        )

    if dark_style is None:
        dark_style = app.config.pygments_dark_style

    return PygmentsBridge("html", dark_style).formatter_args["style"]


def get_pygments_style_colors(
    style: Style, *, fallbacks: Dict[str, str]
) -> Dict[str, str]:
    """Get background/foreground colors for given pygments style."""
    background = style.background_color
    text_colors = style.style_for_token(Text)
    foreground = text_colors["color"]

    if not background:
        background = fallbacks["background"]

    if not foreground:
        foreground = fallbacks["foreground"]
    else:
        foreground = f"#{foreground}"

    return {"background": background, "foreground": foreground}


@lru_cache(maxsize=2)
def get_colors_for_codeblocks(
    highlighter: PygmentsBridge, *, fg: str, bg: str
) -> Dict[str, str]:
    """Get background/foreground colors for given pygments style."""
    return get_pygments_style_colors(
        highlighter.formatter_args["style"],
        fallbacks={
            "foreground": fg,
            "background": bg,
        },
    )


def _get_styles(formatter: HtmlFormatter, *, prefix: str) -> Iterator[str]:
    """Get styles out of a formatter, where everything has the correct prefix."""
    for line in formatter.get_linenos_style_defs():
        yield f"{prefix} {line}"
    yield from formatter.get_background_style_defs(prefix)
    yield from formatter.get_token_style_defs(prefix)


def get_pygments_stylesheet() -> str:
    """Generate the theme-specific pygments.css.

    There is no way to tell Sphinx how the theme handles dark mode; at this time.
    """
    light_formatter = HtmlFormatter(style=_KNOWN_STYLES_IN_USE["light"])
    dark_formatter = HtmlFormatter(style=_KNOWN_STYLES_IN_USE["dark"])

    lines: List[str] = []

    lines.extend(_get_styles(light_formatter, prefix=".highlight"))

    dark_prefix = ":root[theme=dark] .highlight"
    lines.extend(_get_styles(dark_formatter, prefix=dark_prefix))

    return "\n".join(lines)


def _overwrite_pygments_css(
    app: sphinx.application.Sphinx,
    exception: Optional[Exception],
) -> None:
    if exception is not None:
        return

    assert app.builder
    with open(
        os.path.join(app.builder.outdir, "_static", "pygments.css"),
        "w",
        encoding="utf-8",
    ) as f:
        f.write(get_pygments_stylesheet())


def _get_html_theme_path():
    """Return list of HTML theme paths."""
    parent = Path(__file__).parent.resolve()
    theme_path = parent / "theme" / "stmaterial"
    return theme_path


@lru_cache(maxsize=None)
def _asset_hash(path: str) -> str:
    """Append a `?digest=` to an url based on the file content."""
    full_path = _get_html_theme_path() / "static" / path
    digest = hashlib.sha1(full_path.read_bytes()).hexdigest()

    return f"_static/{path}?digest={digest}"


def _add_asset_hashes(static: List[str], add_digest_to: List[str]) -> None:
    for asset in add_digest_to:
        index = static.index("_static/" + asset)
        static[index].filename = _asset_hash(asset)  # type: ignore


def _compute_hide_toc(
    context: Dict[str, Any],
    *,
    builder: StandaloneHTMLBuilder,
    docname: str,
) -> bool:
    # Should the table of contents be hidden?
    file_meta = context.get("meta", None) or {}
    if "hide-toc" in file_meta:
        return True
    elif "toc" not in context:
        return True
    elif not context["toc"]:
        return True

    return False


def _compute_hide_sidenav(
    context: Dict[str, Any],
    *,
    builder: StandaloneHTMLBuilder,
    docname: str,
) -> bool:
    # Should the sidenav be hidden?
    file_meta = context.get("meta", None) or {}
    if "hide-sidenav" in file_meta:
        return True

    if "full-width" in file_meta:
        return True

    return False


def _compute_hide_tocnav(
    context: Dict[str, Any],
    *,
    builder: StandaloneHTMLBuilder,
    docname: str,
) -> bool:
    # Should the sidenav be hidden?
    file_meta = context.get("meta", None) or {}
    if "hide-tocnav" in file_meta:
        return True

    if "full-width" in file_meta:
        return True

    return False


def _html_page_context(
    app: sphinx.application.Sphinx,
    pagename: str,
    templatename: str,
    context: Dict[str, Any],
    doctree: Any,
) -> None:
    if app.config.html_theme != "stmaterial":
        return

    assert isinstance(app.builder, StandaloneHTMLBuilder)

    if "css_files" in context:
        if "_static/styles/stmaterial.css" not in context["css_files"]:
            raise Exception(
                "This documentation is not using `stmaterial.css` as the stylesheet. "
                "If you have set `html_style` in your conf.py file, remove it."
            )

        _add_asset_hashes(
            context["css_files"],
            ["styles/stmaterial.css"],
        )
    if "scripts" in context:
        _add_asset_hashes(
            context["scripts"],
            ["scripts/stmaterial.js"],
        )

    context["hide_toc"] = _compute_hide_toc(
        context, builder=app.builder, docname=pagename
    )
    context["hide_sidenav"] = _compute_hide_sidenav(
        context, builder=app.builder, docname=pagename
    )
    context["hide_tocnav"] = _compute_hide_tocnav(
        context, builder=app.builder, docname=pagename
    )

    # Inject information about styles
    context["stmaterial_pygments"] = {
        "light": get_pygments_style_colors(
            _KNOWN_STYLES_IN_USE["light"],
            fallbacks=dict(
                foreground="black",
                background="white",
            ),
        ),
        "dark": get_pygments_style_colors(
            _KNOWN_STYLES_IN_USE["dark"],
            fallbacks=dict(
                foreground="white",
                background="black",
            ),
        ),
    }

    # Basic constants
    context["theme_version"] = __version__

    # Translations
    translation = get_translation(MESSAGE_CATALOG_NAME)
    context["translate"] = translation


def _builder_inited(app: sphinx.application.Sphinx) -> None:
    if app.config.html_theme != "stmaterial":
        return
    if "stmaterial" in app.config.extensions:
        raise Exception(
            "Did you list 'stmaterial' in the `extensions` in conf.py? "
            "If so, please remove it. stmaterial does not work with non-HTML builders "
            "and specifying it as an `html_theme` is sufficient."
        )

    if not isinstance(app.builder, StandaloneHTMLBuilder):
        raise Exception(
            "stmaterial is being used as an extension in a non-HTML build. "
            "This should not happen."
        )

    builder = app.builder
    assert builder, "what?"
    assert (
        builder.highlighter is not None
    ), "there should be a default style known to Sphinx"
    assert (
        builder.dark_highlighter is None
    ), "this shouldn't be a dark style known to Sphinx"

    update_known_styles_state(app)

    if "ablog" in app.config.extensions:
        if (
            not config_provided_by_user(app, "post_show_prev_next")
            or app.config.post_show_prev_next
        ):
            app.config.post_show_prev_next = False

        else:
            app.config.post_show_prev_next = ""

    def _update_default(key: str, *, new_default: Any) -> None:
        app.config.values[key] = (new_default, *app.config.values[key][1:])

    # Change the default permalinks icon
    _update_default("html_permalinks_icon", new_default="#")


def _update_config(app: sphinx.application.Sphinx) -> None:
    theme_options = get_theme_options(app)

    header_icons = theme_options.get("header_icons", [])
    source_repo = theme_options.get("source_repository", None)
    if not (header_icons) and source_repo:
        header_icons.append(
            {"name": "Github", "url": source_repo, "class": "fa-brands fa-github"}
        )
        theme_options["header_icons"] = header_icons

    else:
        for icon in header_icons:
            svg = icon.get("svg")
            if svg:
                svg = f"_static/{svg}"
                icon["svg"] = svg

    # Add an analytics ID to the site if provided
    analytics = theme_options.get("analytics", {})
    if analytics:
        # Google Analytics
        gid = analytics.get("google_analytics_id")

        if gid:
            gid_js_path = f"https://www.googletagmanager.com/gtag/js?id={gid}"
            gid_script = f"""
                window.dataLayer = window.dataLayer || [];
                function gtag(){{ dataLayer.push(arguments); }}
                gtag('js', new Date());
                gtag('config', '{gid}');
            """

            # Link the JS files
            app.add_js_file(gid_js_path, loading_method="async")
            app.add_js_file(None, body=gid_script)


def update_and_remove_templates(
    app: sphinx.application.Sphinx, pagename: str, templatename: str, context, doctree
) -> None:
    template_sections = [
        "theme_footer",
        "theme_footer_content",
        "theme_article_top_left",
        "theme_article_top_right",
        "theme_article_bottom_left",
        "theme_article_bottom_right",
        "sidebars",
    ]

    for section in template_sections:
        if context.get(section):
            # Break apart `,` separated strings so we can use , in the defaults
            if isinstance(context.get(section), str):
                context[section] = [
                    ii.strip() for ii in context.get(section).split(",")
                ]

            # Add `.html` to templates with no suffix
            for ii, template in enumerate(context.get(section)):
                if not os.path.splitext(template)[1]:
                    context[section][ii] = template + ".html"


def setup(app: sphinx.application.Sphinx) -> Dict[str, Any]:
    """Entry point for sphinx theming."""
    app.require_sphinx("3.0")

    app.add_config_value(
        "pygments_dark_style", default="native", rebuild="env", types=[str]
    )

    theme_dir = _get_html_theme_path()
    app.add_html_theme("stmaterial", theme_dir)

    app.add_post_transform(ShortenLinkTransform)
    app.add_post_transform(WrapTableAndMathInAContainerTransform)
    # Translations
    locale_dir = os.path.join(theme_dir, "static", "locales")
    app.add_message_catalog(MESSAGE_CATALOG_NAME, locale_dir)

    app.connect("html-page-context", _html_page_context)
    app.connect("html-page-context", update_and_remove_templates)
    app.connect("html-page-context", add_toctree_functions)
    app.connect("builder-inited", _builder_inited)
    app.connect("builder-inited", _update_config)
    app.connect("build-finished", _overwrite_pygments_css)
    # Include component templates
    app.config.templates_path.append(str(theme_dir / "components"))
    app.config.html_static_path.append(str(theme_dir / "static/images"))

    app.add_directive("gallery-grid", GalleryDirective)

    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
        "version": __version__,
    }
