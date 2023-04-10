__version__ = "0.0.4"

import hashlib
import logging
import os
import logging
import sphinx.application
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.locale import get_translation
from ._navigation import add_toctree_functions
from ._transforms import ShortenLinkTransform, WrapTableAndMathInAContainerTransform


MESSAGE_CATALOG_NAME = "stmaterial"
logger = logging.getLogger(__name__)


def get_html_theme_path():
    """Return list of HTML theme paths."""
    parent = Path(__file__).parent.resolve()
    theme_path = parent / "theme" / "stmaterial"
    return theme_path


def _get_theme_options(app):
    """Return theme options for the application w/ a fallback if they don't exist.
    In general we want to modify app.builder.theme_options if it exists, so prefer that first.
    """
    if hasattr(app.builder, "theme_options"):
        # In most HTML build cases this will exist except for some circumstances (see below).
        return app.builder.theme_options
    elif hasattr(app.config, "html_theme_options"):
        # For example, linkcheck will have this configured but won't be in builder obj.
        return app.config.html_theme_options
    else:
        # Empty dictionary as a fail-safe.
        return {}


def _config_provided_by_user(app, key):
    """Check if the user has manually provided the config.
    REMOVE when pydata v0.14 is released and import from there.
    """
    return any(key in ii for ii in [app.config.overrides, app.config._raw_config])


@lru_cache(maxsize=None)
def _asset_hash(path: str) -> str:
    """Append a `?digest=` to an url based on the file content."""
    full_path = get_html_theme_path() / "static" / path
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


def _compute_hide_navigation(
    context: Dict[str, Any],
    *,
    builder: StandaloneHTMLBuilder,
    docname: str,
) -> bool:
    # Should the table of contents be hidden?
    file_meta = context.get("meta", None) or {}
    if "hide-navigation" in file_meta:
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
    context["hide_navigation"] = _compute_hide_navigation(
        context, builder=app.builder, docname=pagename
    )
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
            "If so, please remove it. ssdoc does not work with non-HTML builders "
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

    def _update_default(key: str, *, new_default: Any) -> None:
        app.config.values[key] = (new_default, *app.config.values[key][1:])

    # Change the default permalinks icon
    _update_default("html_permalinks_icon", new_default="#")


def _update_config(app: sphinx.application.Sphinx) -> None:
    theme_options = _get_theme_options(app)

    header_icons = theme_options.get("header_icons", [])
    source_repo = theme_options.get("source_repository", None)
    if not(header_icons) and source_repo:
        header_icons.append(
            {"name":"Github", "url": source_repo, "class":"fa-brands fa-github"}
            )
        theme_options["header_icons"] = header_icons

    else:
        for icon in header_icons:
            svg = icon.get("svg")
            if svg:
                svg = f"_static/images/{svg}"
                icon["svg"] = svg


def activate_extensions(app, extensions):
    """Activate extensions bundled with this theme.
    
    This also manually triggers the `config-inited` build step to account for
    added extensions that hook into this event.
    """

    # Remove all of the `config-inited` event listeners because they've already triggered
    # We'll then re-trigger this event after adding extensions so that *only* their event hooks trigger
    old_listeners = app.events.listeners["config-inited"]
    app.events.listeners["config-inited"] = []
    
    for extension in extensions:
        # If it's already been activated just skip it
        if extension in app.config.extensions:
            continue
        app.setup_extension(extension)

    # Emit the config-inited event so that the new extensions run their hooks
    app.emit("config-inited", app.config)

    # Finally join back the lists
    app.events.listeners["config-inited"][:0] = old_listeners
################################################################################



def setup(app: sphinx.application.Sphinx) -> Dict[str, Any]:
    """Entry point for sphinx theming."""
    theme_dir = get_html_theme_path()
    app.add_html_theme("stmaterial", theme_dir)

    app.add_post_transform(ShortenLinkTransform)
    app.add_post_transform(WrapTableAndMathInAContainerTransform)
    # Translations
    locale_dir = os.path.join(theme_dir, "static", "locales")
    app.add_message_catalog(MESSAGE_CATALOG_NAME, locale_dir)

    app.connect("html-page-context", _html_page_context)
    app.connect("builder-inited", _builder_inited)
    app.connect("builder-inited", _update_config)
    app.connect("html-page-context", add_toctree_functions)


    extensions = ["sphinx_design", "sphinx_copybutton", "sphinx_togglebutton", "sphinx_subfigure"]
    activate_extensions(app, extensions)

    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
        "version": __version__,
    }