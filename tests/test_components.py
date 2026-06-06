"""Tests for pyclay component API."""
import pytest
import pyclay as pc
from pyclay import _runtime


def setup_function():
    """Reset runtime state before each test."""
    _runtime.reset()


# ---------------------------------------------------------------------------
# Version
# ---------------------------------------------------------------------------

def test_version_exists():
    assert hasattr(pc, "__version__")
    assert isinstance(pc.__version__, str)
    assert len(pc.__version__.split(".")) == 3


# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------

def test_page_config_defaults():
    pc.page_config(title="Test")
    cfg = _runtime.get_page_config()
    assert cfg["title"] == "Test"
    assert cfg["theme"] == "ivory"


def test_page_config_theme():
    pc.page_config(title="T", theme="obsidian")
    cfg = _runtime.get_page_config()
    assert cfg["theme"] == "obsidian"


def test_page_config_invalid_theme():
    with pytest.raises(AssertionError):
        pc.page_config(title="T", theme="nonexistent")


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------

def test_page_creates_new_page():
    pc.page("Home")
    pc.page("About")
    pages = _runtime.get_pages()
    assert "Home" in pages
    assert "About" in pages


# ---------------------------------------------------------------------------
# Text components
# ---------------------------------------------------------------------------

def test_heading():
    pc.heading("Hello", level=2)
    tree = _runtime.get_tree()
    assert len(tree) == 1
    assert tree[0]["type"] == "heading"
    assert tree[0]["text"] == "Hello"
    assert tree[0]["level"] == 2


def test_text():
    pc.text("paragraph content")
    tree = _runtime.get_tree()
    assert len(tree) == 1
    assert tree[0]["type"] == "paragraph"
    assert tree[0]["text"] == "paragraph content"


def test_blockquote():
    pc.blockquote("a quote")
    tree = _runtime.get_tree()
    assert tree[0]["type"] == "blockquote"
    assert tree[0]["text"] == "a quote"


# ---------------------------------------------------------------------------
# Lists
# ---------------------------------------------------------------------------

def test_bullet_list():
    pc.bullet_list(["a", "b", "c"])
    tree = _runtime.get_tree()
    assert tree[0]["type"] == "bullet_list"
    assert tree[0]["items"] == ["a", "b", "c"]


def test_ordered_list():
    pc.ordered_list(["x", "y"])
    tree = _runtime.get_tree()
    assert tree[0]["type"] == "ordered_list"


# ---------------------------------------------------------------------------
# UI components
# ---------------------------------------------------------------------------

def test_card():
    pc.card(title="T", body="B")
    tree = _runtime.get_tree()
    assert tree[0]["type"] == "card"
    assert tree[0]["title"] == "T"
    assert tree[0]["body"] == "B"


def test_badge():
    pc.badge("v1", color="#fff")
    tree = _runtime.get_tree()
    assert tree[0]["type"] == "badge"
    assert tree[0]["color"] == "#fff"


def test_alert_variants():
    for v in ("info", "success", "warning", "error"):
        _runtime.reset()
        pc.alert("msg", variant=v)
        tree = _runtime.get_tree()
        assert tree[0]["variant"] == v


def test_button():
    pc.button("Click me")
    tree = _runtime.get_tree()
    assert tree[0]["type"] == "button"
    assert tree[0]["label"] == "Click me"


def test_link_button():
    pc.link_button("Go", "/page")
    tree = _runtime.get_tree()
    assert tree[0]["type"] == "link_button"
    assert tree[0]["href"] == "/page"


# ---------------------------------------------------------------------------
# Data display
# ---------------------------------------------------------------------------

def test_table():
    pc.table(["A", "B"], [["1", "2"]])
    tree = _runtime.get_tree()
    assert tree[0]["type"] == "table"
    assert tree[0]["headers"] == ["A", "B"]


def test_metric():
    pc.metric("Sales", "$1M", delta="+5%", delta_color="green")
    tree = _runtime.get_tree()
    assert tree[0]["type"] == "metric"
    assert tree[0]["delta"] == "+5%"


def test_progress_bar():
    pc.progress_bar(75, label="Done")
    tree = _runtime.get_tree()
    assert tree[0]["type"] == "progress_bar"
    assert tree[0]["value"] == 75


# ---------------------------------------------------------------------------
# Media
# ---------------------------------------------------------------------------

def test_image():
    pc.image("test.jpg", alt="pic", width=100)
    tree = _runtime.get_tree()
    assert tree[0]["type"] == "image"
    assert tree[0]["src"] == "test.jpg"


def test_video():
    pc.video("test.mp4", controls=True)
    tree = _runtime.get_tree()
    assert tree[0]["type"] == "video"
    assert tree[0]["controls"] is True


def test_code_block():
    pc.code_block("print('hi')", language="python")
    tree = _runtime.get_tree()
    assert tree[0]["type"] == "code_block"
    assert tree[0]["language"] == "python"


# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------

def test_container_context():
    with pc.container():
        pc.text("inside")
    tree = _runtime.get_tree()
    assert tree[0]["type"] == "container"
    assert len(tree[0]["children"]) == 1
    assert tree[0]["children"][0]["text"] == "inside"


def test_columns_context():
    with pc.columns([1, 2]):
        with pc.column():
            pc.text("col1")
        with pc.column():
            pc.text("col2")
    tree = _runtime.get_tree()
    assert tree[0]["type"] == "container"
    assert "1fr 2fr" in tree[0]["style"]["grid_template_columns"]
    assert len(tree[0]["children"]) == 2


# ---------------------------------------------------------------------------
# Navigation
# ---------------------------------------------------------------------------

def test_navbar():
    pc.navbar("My App", links=[{"text": "Home", "href": "#home"}])
    tree = _runtime.get_tree()
    assert tree[0]["type"] == "navbar"
    assert tree[0]["title"] == "My App"


def test_footer():
    pc.footer(text="© 2026", variant="simple")
    tree = _runtime.get_tree()
    assert tree[0]["type"] == "footer"


# ---------------------------------------------------------------------------
# Accordion & Tabs
# ---------------------------------------------------------------------------

def test_accordion():
    pc.accordion([{"title": "Q", "content": "A"}])
    tree = _runtime.get_tree()
    assert tree[0]["type"] == "accordion"
    assert len(tree[0]["items"]) == 1


def test_tabs_and_panels():
    pc.tabs(["A", "B"])
    with pc.tab_panel():
        pc.text("Panel A")
    with pc.tab_panel():
        pc.text("Panel B")
    tree = _runtime.get_tree()
    tab_comp = tree[0]
    assert tab_comp["type"] == "tabs"
    assert len(tab_comp["panels"]) == 2


# ---------------------------------------------------------------------------
# Style passthrough
# ---------------------------------------------------------------------------

def test_style_dict_passthrough():
    pc.heading("Styled", style={"color": "red", "margin_top": "2rem"})
    tree = _runtime.get_tree()
    assert tree[0]["style"]["color"] == "red"
    assert tree[0]["style"]["margin_top"] == "2rem"


# ---------------------------------------------------------------------------
# Utility
# ---------------------------------------------------------------------------

def test_spacer():
    pc.spacer("2rem")
    tree = _runtime.get_tree()
    assert tree[0]["type"] == "spacer"
    assert tree[0]["height"] == "2rem"


def test_divider():
    pc.divider()
    tree = _runtime.get_tree()
    assert tree[0]["type"] == "divider"
