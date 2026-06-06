"""
pyclay – public API
====================
Every function appends a component dict to the runtime tree.
An optional ``style`` dict lets callers control CSS per-element.
"""

__version__ = "1.1.1"

from contextlib import contextmanager
from pyclay import _runtime


# Page config

_VALID_THEMES = {"ivory", "nebula", "arctic", "obsidian"}

def page_config(*, title="My App", theme="ivory", favicon="", custom_css="", theme_switcher=True):
    """Set page-level settings.  Call once, at the top of your script.

    Args:
        title:          Browser tab title.
        theme:          ``"ivory"``, ``"nebula"``, ``"arctic"``, or ``"obsidian"``.
        favicon:        URL to a favicon image (optional).
        custom_css:     Path or URL to a custom CSS file (optional).
        theme_switcher: If True, renders a theme selector dropdown in the navbar
                        (or floating) to switch themes live. (default: True).
    """
    assert theme in _VALID_THEMES, f"theme must be one of {_VALID_THEMES}"
    _runtime.set_page_config(title=title, theme=theme, favicon=favicon, custom_css=custom_css, theme_switcher=theme_switcher)


def page(name):
    """Switch context to build a new page. Subsequent elements belong to this page.

    Args:
        name: Unique page identifier/label (e.g. "Docs" or "Components").
    """
    _runtime.set_current_page(name)


# Text

def heading(text, level=1, *, style=None):
    assert 1 <= level <= 6, "Heading level must be 1-6"
    _runtime.add({"type": "heading", "text": text, "level": level, "style": style})


def text(content, *, style=None):
    _runtime.add({"type": "paragraph", "text": content, "style": style})


def bold(content, *, style=None):
    _runtime.add({"type": "bold", "text": content, "style": style})


def italic(content, *, style=None):
    _runtime.add({"type": "italic", "text": content, "style": style})


def blockquote(content, *, style=None):
    _runtime.add({"type": "blockquote", "text": content, "style": style})


def kbd(text_content):
    """Render a keyboard-key style element."""
    _runtime.add({"type": "kbd", "text": text_content})


# Lists

def bullet_list(items, *, style=None):
    assert isinstance(items, list), "bullet_list expects a list"
    _runtime.add({"type": "bullet_list", "items": items, "style": style})


def ordered_list(items, *, style=None):
    assert isinstance(items, list), "ordered_list expects a list"
    _runtime.add({"type": "ordered_list", "items": items, "style": style})


# Media / embeds

def image(src, *, alt="", width=None, height=None, style=None):
    _runtime.add({"type": "image", "src": src, "alt": alt, "width": width, "height": height, "style": style})


def video(src, *, autoplay=False, loop=False, controls=True, width=None, height=None, style=None):
    """Render a video element.

    Args:
        src:      URL or path to the video (e.g. "assets/video.mp4").
        autoplay: If True, play automatically (will be muted for browser compliance).
        loop:     If True, play in a loop.
        controls: If True, display playback controls.
        width:    Optional width of the video.
        height:   Optional height of the video.
        style:    Optional style overrides dictionary.
    """
    _runtime.add({
        "type": "video",
        "src": src,
        "autoplay": autoplay,
        "loop": loop,
        "controls": controls,
        "width": width,
        "height": height,
        "style": style
    })



def link(text, href, *, style=None):
    _runtime.add({"type": "link", "text": text, "href": href, "style": style})


def code_block(code, *, language="", style=None):
    _runtime.add({"type": "code_block", "code": code, "language": language, "style": style})


def html_raw(markup):
    """Inject arbitrary HTML.  Use with care."""
    _runtime.add({"type": "raw", "html": markup})


# Decorative

def divider(*, style=None):
    _runtime.add({"type": "divider", "style": style})


def spacer(height="1rem"):
    _runtime.add({"type": "spacer", "height": height})


# Data display

def table(headers, rows, *, style=None):
    """Render an HTML table.

    Args:
        headers: List of column header strings.
        rows:    List of rows, each row a list of cell values.
    """
    _runtime.add({"type": "table", "headers": headers, "rows": rows, "style": style})


def metric(label, value, *, delta=None, delta_color=None, style=None):
    """Streamlit-style metric card.

    Args:
        label:       Metric title.
        value:       Primary value to display.
        delta:       Optional delta string (e.g. "+12%").
        delta_color: ``"green"`` (default for positive) or ``"red"``.
    """
    _runtime.add({
        "type": "metric",
        "label": label,
        "value": value,
        "delta": delta,
        "delta_color": delta_color,
        "style": style,
    })


def progress_bar(value, *, max_value=100, label="", style=None):
    _runtime.add({
        "type": "progress_bar",
        "value": value,
        "max": max_value,
        "label": label,
        "style": style,
    })


# UI elements

def badge(text, *, color="#6366f1", style=None):
    _runtime.add({"type": "badge", "text": text, "color": color, "style": style})


def alert(text, *, variant="info", style=None):
    """Alert box.  ``variant`` is one of: info, success, warning, error."""
    _runtime.add({"type": "alert", "text": text, "variant": variant, "style": style})


def button(label, *, style=None):
    """Visual-only styled button (no click handler)."""
    _runtime.add({"type": "button", "label": label, "style": style})


def link_button(label, href, *, style=None):
    """An anchor element styled as a button.  Navigates to *href* on click."""
    _runtime.add({"type": "link_button", "label": label, "href": href, "style": style})


def card(title="", body="", *, style=None):
    """A bordered card container.  Accepts plain text title/body."""
    _runtime.add({"type": "card", "title": title, "body": body, "style": style})


# Collapsible / Tabs

def accordion(items, *, style=None):
    """Collapsible accordion using ``<details>/<summary>``.

    Args:
        items: List of ``{"title": "...", "content": "..."}`` dicts.
    """
    assert isinstance(items, list), "accordion expects a list of items"
    _runtime.add({"type": "accordion", "items": items, "style": style})


def tabs(labels, *, style=None):
    """Begin a tabbed section.  Follow with ``tab_panel()`` context managers.

    Args:
        labels: List of tab label strings, one per panel.
    """
    assert isinstance(labels, list) and len(labels) >= 1, "tabs expects a list of labels"
    comp = {"type": "tabs", "labels": labels, "panels": [], "style": style}
    _runtime.add(comp)
    _runtime._tabs_stack.append(comp)


@contextmanager
def tab_panel(*, style=None):
    """Context manager for a single tab panel inside a ``tabs()`` block."""
    assert _runtime._tabs_stack, "tab_panel() must be used after a tabs() call"
    panel = {"type": "container", "children": [], "style": style}
    _runtime._tabs_stack[-1]["panels"].append(panel)
    _runtime._container_stack.append(panel["children"])
    try:
        yield
    finally:
        _runtime._container_stack.pop()
        # Pop tabs_stack when all panels are defined
        if len(_runtime._tabs_stack[-1]["panels"]) >= len(_runtime._tabs_stack[-1]["labels"]):
            _runtime._tabs_stack.pop()


# Navbar & Footer

_VALID_NAV_VARIANTS = {"simple", "centered"}
_VALID_FOOTER_VARIANTS = {"simple", "columns"}

def navbar(title="", links=None, *, variant="simple", style=None):
    """Add a navigation bar to the top of the page.

    Args:
        title:   Brand / logo text.
        links:   List of ``{"text": "...", "href": "..."}`` dicts.
        variant: ``"simple"`` (logo left, links right) or
                 ``"centered"`` (logo centred, links below).
    """
    assert variant in _VALID_NAV_VARIANTS, f"navbar variant must be one of {_VALID_NAV_VARIANTS}"
    _runtime.add({
        "type": "navbar",
        "title": title,
        "links": links or [],
        "variant": variant,
        "style": style,
    })


def footer(text="", links=None, *, variant="simple", columns_data=None, style=None):
    """Add a footer to the bottom of the page.

    Args:
        text:         Main footer text (copyright line, etc.).
        links:        List of ``{"text": "...", "href": "..."}`` dicts.
        variant:      ``"simple"`` (single line) or ``"columns"`` (multi-column).
        columns_data: For ``"columns"`` variant only -- list of
                      ``{"heading": "...", "links": [{"text": ..., "href": ...}, ...]}`` dicts.
    """
    assert variant in _VALID_FOOTER_VARIANTS, f"footer variant must be one of {_VALID_FOOTER_VARIANTS}"
    _runtime.add({
        "type": "footer",
        "text": text,
        "links": links or [],
        "variant": variant,
        "columns_data": columns_data or [],
        "style": style,
    })


# Layout: container & columns

@contextmanager
def container(*, style=None):
    """Context manager -- wraps children in a styled ``<div>``."""
    comp = {"type": "container", "children": [], "style": style}
    _runtime.push_container(comp)
    try:
        yield
    finally:
        _runtime.pop_container()


@contextmanager
def columns(ratios=None, *, gap="1rem", style=None):
    """Context manager -- CSS-grid columns.

    ``ratios`` is a list of relative widths, e.g. ``[1, 2]`` -> ``1fr 2fr``.
    Use nested ``column()`` calls inside.
    """
    if ratios is None:
        ratios = [1, 1]
    template = " ".join(f"{r}fr" for r in ratios)
    merged = style or {}
    merged = {
        "display": "grid",
        "grid_template_columns": template,
        "gap": gap,
        **merged,
    }
    comp = {"type": "container", "children": [], "style": merged}
    _runtime.push_container(comp)
    try:
        yield
    finally:
        _runtime.pop_container()


@contextmanager
def column(*, style=None):
    """A single column inside a ``columns()`` block."""
    merged = style or {}
    merged = {"min_width": "0", **merged}
    comp = {"type": "container", "children": [], "style": merged}
    _runtime.push_container(comp)
    try:
        yield
    finally:
        _runtime.pop_container()

