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
