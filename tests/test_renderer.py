"""Tests for the HTML renderer."""
from pyclay import _runtime, _renderer
import pyclay as pc


def setup_function():
    _runtime.reset()


def test_render_produces_html():
    """render_page() should return a valid HTML string."""
    pc.page_config(title="Test Page", theme="ivory")
    pc.heading("Hello")
    pc.text("World")
    html = _renderer.render_page()
    assert "<!DOCTYPE html>" in html or "<!doctype html>" in html.lower()
    assert "<html" in html
    assert "Hello" in html
    assert "World" in html


def test_render_includes_title():
    pc.page_config(title="My Title")
    html = _renderer.render_page()
    assert "<title>My Title</title>" in html


def test_render_multi_page():
    """Multi-page apps should include all page content."""
    pc.page_config(title="Multi")
    pc.page("Home")
    pc.heading("Home Page")
    pc.page("About")
    pc.heading("About Page")
    html = _renderer.render_page()
    assert "Home Page" in html
    assert "About Page" in html


def test_render_theme_applied():
    """The selected theme name should appear in the rendered output."""
    pc.page_config(title="T", theme="obsidian")
    html = _renderer.render_page()
    assert "obsidian" in html.lower()


def test_render_code_block_escaped():
    """Code block content with HTML chars should be escaped."""
    pc.code_block("<script>alert('xss')</script>", language="html")
    html = _renderer.render_page()
    # The raw <script> should NOT appear unescaped
    assert "<script>alert(" not in html


def test_render_theme_sync_js_included():
    """The theme sync JS should be included in the rendered output."""
    pc.page_config(title="T", theme="obsidian")
    html = _renderer.render_page()
    assert "const currentTheme = root.getAttribute('data-theme');" in html


def test_render_theme_switcher_disabled():
    """When theme_switcher is False, the theme toggle elements and JS are omitted."""
    pc.page_config(title="T", theme="nebula", theme_switcher=False)
    pc.navbar("My Brand")
    html = _renderer.render_page()
    # Navbar shouldn't contain the dropdown
    assert 'class="theme-dropdown"' not in html
    # The theme switcher JS should not be loaded
    assert "labels = { ivory: 'Ivory'" not in html
    # But the default theme attribute is still applied
    assert 'data-theme="nebula"' in html


def test_render_sidebar_resources():
    """Verify that navbar sidebar CSS and JS resources are present in the HTML output."""
    pc.page_config(title="Test Page")
    pc.navbar("Test Brand")
    html = _renderer.render_page()
    assert ".navbar-sidebar-close" in html
    assert ".navbar-backdrop" in html
    assert "navbar-backdrop" in html  # checking JS

