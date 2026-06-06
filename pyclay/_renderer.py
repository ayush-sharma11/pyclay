"""
pyclay - HTML renderer
=======================
Converts the component tree into a full HTML page with a modern,
polished default stylesheet supporting four themes:
  - ivory     (vibrant indigo accent, warm white bg, Inter)
  - nebula    (deep navy/purple tones, Inter)
  - arctic    (minimal, clean, Geist-inspired light)
  - obsidian  (pure black, sharp contrast, Geist-inspired dark)
"""

import html as _html
import re as _re
from pyclay import _runtime

_tab_id_counter = 0


# Helpers
def _style_to_css(style_dict):
    """Convert a Python style dict to an inline CSS string.

    Keys use underscores (``font_size``), which are converted to dashes
    (``font-size``).  Returns an empty string when *style_dict* is falsy.
    """
    if not style_dict:
        return ""
    pairs = []
    for key, val in style_dict.items():
        css_prop = key.replace("_", "-")
        pairs.append(f"{css_prop}: {val}")
    return "; ".join(pairs)


def _attr(style_dict):
    """Return a ``style="..."`` attribute string, or empty."""
    css = _style_to_css(style_dict)
    return f' style="{css}"' if css else ""


def _format_style_dim(val):
    if val is None:
        return None
    val_str = str(val).strip()
    if val_str.isdigit():
        return f"{val_str}px"
    return val_str


def _esc(text):
    """HTML-escape user text."""
    return _html.escape(str(text))


def _render_inline_markdown(text):
    """HTML-escape text and parse basic inline markdown formatting:
    **bold**, *italic*, `kbd`, and [text](url).
    """
    escaped = _esc(text)
    # Parse bold **text**
    escaped = _re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', escaped)
    # Parse italic *text*
    escaped = _re.sub(r'\*(.*?)\*', r'<em>\1</em>', escaped)
    # Parse inline kbd/code `text`
    escaped = _re.sub(r'`(.*?)`', r'<kbd>\1</kbd>', escaped)
    # Parse link [text](url)
    escaped = _re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', escaped)
    return escaped


# Component renderers
def render_component(c):
    t = c["type"]

    # Text
    if t == "heading":
        tag = f"h{c['level']}"
        return f"<{tag}{_attr(c.get('style'))}>{_render_inline_markdown(c['text'])}</{tag}>"

    if t == "paragraph":
        return f"<p{_attr(c.get('style'))}>{_render_inline_markdown(c['text'])}</p>"

    if t == "bold":
        return f"<strong{_attr(c.get('style'))}>{_render_inline_markdown(c['text'])}</strong>"

    if t == "italic":
        return f"<em{_attr(c.get('style'))}>{_render_inline_markdown(c['text'])}</em>"

    if t == "blockquote":
        return f"<blockquote{_attr(c.get('style'))}>{_render_inline_markdown(c['text'])}</blockquote>"

    if t == "kbd":
        return f"<kbd>{_render_inline_markdown(c['text'])}</kbd>"

    # Lists
    if t == "bullet_list":
        items = "".join(f"<li>{_render_inline_markdown(i)}</li>" for i in c["items"])
        return f"<ul{_attr(c.get('style'))}>{items}</ul>"

    if t == "ordered_list":
        items = "".join(f"<li>{_render_inline_markdown(i)}</li>" for i in c["items"])
        return f"<ol{_attr(c.get('style'))}>{items}</ol>"

    # Media / embeds
    if t == "image":
        style = dict(c.get("style") or {})
        if c.get("width") is not None:
            style["width"] = _format_style_dim(c["width"])
        if c.get("height") is not None:
            style["height"] = _format_style_dim(c["height"])
        return f'<img src="{_esc(c["src"])}" alt="{_esc(c.get("alt", ""))}" loading="lazy"{_attr(style)} />'

    if t == "video":
        autoplay = " autoplay" if c.get("autoplay") else ""
        loop = " loop" if c.get("loop") else ""
        controls = " controls" if c.get("controls", True) else ""
        muted = " muted" if c.get("autoplay") else ""
        style = dict(c.get("style") or {})
        if c.get("width") is not None:
            style["width"] = _format_style_dim(c["width"])
        if c.get("height") is not None:
            style["height"] = _format_style_dim(c["height"])
        return f'<video src="{_esc(c["src"])}"{controls}{autoplay}{loop}{muted}{_attr(style)}></video>'

    if t == "link":
        return f'<a href="{_esc(c["href"])}"{_attr(c.get("style"))}>{_render_inline_markdown(c["text"])}</a>'

    if t == "code_block":
        lang = c.get("language", "")
        return f'<pre{_attr(c.get("style"))}><code class="language-{_esc(lang)}">{_esc(c["code"])}</code></pre>'

    if t == "raw":
        return c.get("html", "")

    # Decorative
    if t == "divider":
        return f"<hr{_attr(c.get('style'))} />"

    if t == "spacer":
        h = c.get("height", "1rem")
        return f'<div style="height: {h}"></div>'

    # Data display
    if t == "table":
        ths = "".join(f"<th>{_esc(h)}</th>" for h in c["headers"])
        rows_html = ""
        for row in c["rows"]:
            tds = "".join(f"<td>{_esc(cell)}</td>" for cell in row)
            rows_html += f"<tr>{tds}</tr>"
        return (
            f'<div class="table-wrap">'
            f'<table{_attr(c.get("style"))}>'
            f"<thead><tr>{ths}</tr></thead>"
            f"<tbody>{rows_html}</tbody>"
            f"</table></div>"
        )

    if t == "metric":
        delta_html = ""
        if c.get("delta") is not None:
            dc = c.get("delta_color") or ("green" if str(c["delta"]).startswith("+") else "red")
            delta_html = f'<span class="metric-delta" style="color: {dc}">{_esc(c["delta"])}</span>'
        return (
            f'<div class="metric-card"{_attr(c.get("style"))}>'
            f'<span class="metric-label">{_render_inline_markdown(c["label"])}</span>'
            f'<span class="metric-value">{_esc(c["value"])}</span>'
            f'{delta_html}'
            f'</div>'
        )

    if t == "progress_bar":
        pct = min(100, max(0, (c["value"] / c["max"]) * 100))
        label_html = f'<span class="progress-label">{_render_inline_markdown(c["label"])}</span>' if c.get("label") else ""
        return (
            f'<div class="progress-wrap"{_attr(c.get("style"))}>'
            f'{label_html}'
            f'<div class="progress-track">'
            f'<div class="progress-fill" style="width:{pct:.1f}%"></div>'
            f'</div>'
            f'</div>'
        )

    # UI elements
    if t == "badge":
        color = c.get("color", "#6366f1")
        base = f"background:{color}; color:#fff; padding:2px 10px; border-radius:999px; font-size:0.8rem; font-weight:600; display:inline-block;"
        extra = _style_to_css(c.get("style"))
        combined = base + (" " + extra if extra else "")
        return f'<span style="{combined}">{_render_inline_markdown(c["text"])}</span>'

    if t == "alert":
        variant = c.get("variant", "info")
        return (
            f'<div class="alert alert-{_esc(variant)}"{_attr(c.get("style"))}>'
            f'{_render_inline_markdown(c["text"])}'
            f'</div>'
        )

    if t == "button":
        return f'<button class="btn"{_attr(c.get("style"))}>{_esc(c["label"])}</button>'

    if t == "card":
        title_html = f'<div class="card-title">{_render_inline_markdown(c["title"])}</div>' if c.get("title") else ""
        body_html = f'<div class="card-body">{_render_inline_markdown(c["body"])}</div>' if c.get("body") else ""
        return (
            f'<div class="card"{_attr(c.get("style"))}>'
            f'{title_html}{body_html}'
            f'</div>'
        )

    if t == "link_button":
        return f'<a class="btn"{_attr(c.get("style"))} href="{_esc(c["href"])}">{_esc(c["label"])}</a>'

    # Accordion
    if t == "accordion":
        details_html = []
        for item in c.get("items", []):
            details_html.append(
                f'<details class="accordion-item">'
                f'<summary class="accordion-summary">{_render_inline_markdown(item.get("title", ""))}'
                f'<svg class="accordion-chevron" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"></polyline></svg>'
                f'</summary>'
                f'<div class="accordion-content">{_render_inline_markdown(item.get("content", ""))}</div>'
                f'</details>'
            )
        return f'<div class="accordion"{_attr(c.get("style"))}>{"".join(details_html)}</div>'

    # Tabs
    if t == "tabs":
        global _tab_id_counter
        tab_id = f"pctabs-{_tab_id_counter}"
        _tab_id_counter += 1
        labels = c.get("labels", [])
        panels = c.get("panels", [])
        btns = []
        for i, label in enumerate(labels):
            active_cls = ' active' if i == 0 else ''
            btns.append(f'<button class="tab-btn{active_cls}" data-tab-idx="{i}" data-tab-group="{tab_id}">{_esc(label)}</button>')
        btns_html = f'<div class="tab-buttons">{"".join(btns)}</div>'
        pnls = []
        for i, panel in enumerate(panels):
            display = 'block' if i == 0 else 'none'
            children_html = "\n".join(render_component(child) for child in panel.get("children", []))
            pnls.append(f'<div class="tab-panel" data-tab-panel="{i}" data-tab-group="{tab_id}" style="display:{display}">{children_html}</div>')
        pnls_html = "\n".join(pnls)
        return f'<div class="tabs-container"{_attr(c.get("style"))}>{btns_html}\n{pnls_html}</div>'

    # Layout
    if t == "container":
        children_html = "\n".join(render_component(child) for child in c.get("children", []))
        return f'<div{_attr(c.get("style"))}>{children_html}</div>'

    # Navbar & Footer
    if t == "navbar":
        theme = _runtime.get_page_config().get("theme", "ivory")
        theme_switcher = _runtime.get_page_config().get("theme_switcher", True)
        dropdown_html = _build_theme_dropdown_html(theme) if theme_switcher else ""
        links_html = "".join(f'<a href="{_esc(link["href"])}">{_esc(link["text"])}</a>' for link in c.get("links", []))
        links_html += dropdown_html
        hamburger_svg = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>'
        return (
            f'<nav class="navbar navbar-{_esc(c.get("variant", "simple"))}"{_attr(c.get("style"))}>'
            f'<div class="navbar-inner">'
            f'<div class="navbar-brand">{_esc(c.get("title", ""))}</div>'
            f'<button class="navbar-toggle" aria-label="Toggle navigation">{hamburger_svg}</button>'
            f'<div class="navbar-links">{links_html}</div>'
            f'</div>'
            f'</nav>'
        )

    if t == "footer":
        links_html = "".join(f'<a href="{_esc(link["href"])}">{_esc(link["text"])}</a>' for link in c.get("links", []))
        variant = c.get("variant", "simple")
        if variant == "columns":
            cols_html = []
            for col in c.get("columns_data", []):
                col_links = "".join(f'<a href="{_esc(link["href"])}">{_esc(link["text"])}</a>' for link in col.get("links", []))
                heading_html = f'<span class="footer-col-heading">{_esc(col.get("heading", ""))}</span>' if col.get("heading") else ""
                cols_html.append(f'<div class="footer-col">{heading_html}{col_links}</div>')
            grid_html = f'<div class="footer-grid">{"".join(cols_html)}</div>'
            bottom_html = (
                f'<div class="footer-bottom">'
                f'<div>{_esc(c.get("text", ""))}</div>'
                f'<div class="footer-links">{links_html}</div>'
                f'</div>'
            )
            return (
                f'<footer class="site-footer footer-columns"{_attr(c.get("style"))}>'
                f'<div class="footer-inner">'
                f'{grid_html}{bottom_html}'
                f'</div>'
                f'</footer>'
            )
        else:
            return (
                f'<footer class="site-footer footer-simple"{_attr(c.get("style"))}>'
                f'<div class="footer-inner">'
                f'<div>{_esc(c.get("text", ""))}</div>'
                f'<div class="footer-links">{links_html}</div>'
                f'</div>'
                f'</footer>'
            )

    return ""


# Theme System

_THEME_VARS = {
    # Ivory (warm white, indigo accents)
    "ivory": """
    --bg:          #f8f9fc;
    --bg-surface:  #ffffff;
    --fg:          #1e1e2e;
    --fg-muted:    #6c6f85;
    --border:      #e0e2ec;
    --accent:      #6366f1;
    --accent-soft: #eef0ff;
    --radius:      10px;
    --shadow:      0 1px 3px rgba(0,0,0,.06), 0 1px 2px rgba(0,0,0,.04);
    --shadow-lg:   0 10px 30px rgba(0,0,0,.08);

    --alert-info-bg:    #eef4ff;  --alert-info-border:    #3b82f6; --alert-info-fg:    #1e40af;
    --alert-success-bg: #ecfdf5;  --alert-success-border: #10b981; --alert-success-fg: #065f46;
    --alert-warning-bg: #fffbeb;  --alert-warning-border: #f59e0b; --alert-warning-fg: #92400e;
    --alert-error-bg:   #fef2f2;  --alert-error-border:   #ef4444; --alert-error-fg:   #991b1b;

    --gradient-accent: var(--accent);
    --gradient-progress: var(--accent);
    """,

    # Nebula (deep navy/purple)
    "nebula": """
    --bg:          #0f0f17;
    --bg-surface:  #1a1a2e;
    --fg:          #e4e4f0;
    --fg-muted:    #8888a4;
    --border:      #2a2a40;
    --accent:      #818cf8;
    --accent-soft: #1e1e3a;
    --radius:      10px;
    --shadow:      0 1px 3px rgba(0,0,0,.3);
    --shadow-lg:   0 10px 30px rgba(0,0,0,.4);

    --alert-info-bg:    #1e2a4a;  --alert-info-border:    #3b82f6; --alert-info-fg:    #93b4f8;
    --alert-success-bg: #0f2920;  --alert-success-border: #10b981; --alert-success-fg: #6ee7b7;
    --alert-warning-bg: #2c2614;  --alert-warning-border: #f59e0b; --alert-warning-fg: #fcd34d;
    --alert-error-bg:   #2d1515;  --alert-error-border:   #ef4444; --alert-error-fg:   #fca5a5;

    --gradient-accent: var(--accent);
    --gradient-progress: var(--accent);
    """,

    # Arctic (clean, minimal light)
    "arctic": """
    --bg:          #fafafa;
    --bg-surface:  #ffffff;
    --fg:          #171717;
    --fg-muted:    #666666;
    --border:      #eaeaea;
    --accent:      #000000;
    --accent-soft: #f5f5f5;
    --radius:      8px;
    --shadow:      0 1px 2px rgba(0,0,0,.04);
    --shadow-lg:   0 8px 30px rgba(0,0,0,.08);

    --alert-info-bg:    #f0f7ff;  --alert-info-border:    #0070f3; --alert-info-fg:    #0050b3;
    --alert-success-bg: #f0fdf4;  --alert-success-border: #22c55e; --alert-success-fg: #166534;
    --alert-warning-bg: #fffbeb;  --alert-warning-border: #eab308; --alert-warning-fg: #854d0e;
    --alert-error-bg:   #fef2f2;  --alert-error-border:   #ef4444; --alert-error-fg:   #991b1b;

    --gradient-accent: var(--accent);
    --gradient-progress: var(--accent);
    """,

    # Obsidian (pure black, sharp contrast)
    "obsidian": """
    --bg:          #000000;
    --bg-surface:  #111111;
    --fg:          #ededed;
    --fg-muted:    #888888;
    --border:      #222222;
    --accent:      #ffffff;
    --accent-soft: #1a1a1a;
    --radius:      8px;
    --shadow:      0 1px 2px rgba(0,0,0,.4);
    --shadow-lg:   0 8px 30px rgba(0,0,0,.6);

    --alert-info-bg:    #0a1929;  --alert-info-border:    #0070f3; --alert-info-fg:    #6cb6ff;
    --alert-success-bg: #0a1f0d;  --alert-success-border: #22c55e; --alert-success-fg: #4ade80;
    --alert-warning-bg: #1f1a0a;  --alert-warning-border: #eab308; --alert-warning-fg: #facc15;
    --alert-error-bg:   #1f0a0a;  --alert-error-border:   #ef4444; --alert-error-fg:   #f87171;

    --gradient-accent: var(--accent);
    --gradient-progress: var(--accent);
    """,
}


_BASE_CSS = r"""
/* Reset & base  */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html { scroll-behavior: smooth; }

body {
  font-family: var(--font);
  background: var(--bg);
  color: var(--fg);
  line-height: 1.7;
  margin: 0;
  padding: 0;
  -webkit-font-smoothing: antialiased;
  transition: background .2s ease, color .2s ease;
}

.content-wrapper {
  max-width: 860px;
  margin: 0 auto;
  padding: 48px 24px 80px;
}

/* Typography  */
h1, h2, h3, h4, h5, h6 {
  line-height: 1.25;
  font-weight: 700;
  margin: 2rem 0 0.75rem;
  color: var(--fg);
  letter-spacing: -0.02em;
}
h1 { font-size: 2.5rem; }
h2 { font-size: 1.85rem; }
h3 { font-size: 1.45rem; }
h4 { font-size: 1.15rem; }

p   { margin: 0.6rem 0; color: var(--fg); }
a   { color: var(--accent); text-decoration: none; font-weight: 500; transition: opacity .2s ease; }
a:hover { opacity: .75; text-decoration: underline; }

strong { font-weight: 700; }
em     { font-style: italic; }

blockquote {
  border-left: 4px solid var(--accent);
  padding: 0.8rem 1.2rem;
  margin: 1rem 0;
  background: var(--accent-soft);
  border-radius: 0 var(--radius) var(--radius) 0;
  color: var(--fg-muted);
  font-style: italic;
}

kbd {
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 2px 7px;
  font-family: var(--mono);
  font-size: 0.85em;
  box-shadow: 0 1px 0 var(--border);
}

/* Lists  */
ul, ol {
  margin: 0.8rem 0;
  padding-left: 1.6rem;
}
li {
  margin: 0.35rem 0;
  line-height: 1.65;
}
ul li::marker { color: var(--accent); }
ol li::marker { color: var(--accent); font-weight: 600; }

/* Divider  */
hr {
  border: none;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--border), transparent);
  margin: 2rem 0;
}

/* Code  */
pre {
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1rem 1.25rem;
  overflow-x: auto;
  margin: 1rem 0;
  box-shadow: var(--shadow);
  transition: box-shadow .2s ease, border-color .2s ease;
}
pre:hover { box-shadow: var(--shadow-lg); border-color: var(--accent); }

code {
  font-family: var(--mono);
  font-size: 0.9em;
  line-height: 1.6;
}

/* Table  */
.table-wrap {
  overflow-x: auto;
  margin: 1rem 0;
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  border: 1px solid var(--border);
}
table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.92rem;
}
thead {
  background: var(--accent-soft);
}
th {
  text-align: left;
  padding: 0.75rem 1rem;
  font-weight: 600;
  color: var(--accent);
  border-bottom: 2px solid var(--border);
}
td {
  padding: 0.65rem 1rem;
  border-bottom: 1px solid var(--border);
}
tbody tr { transition: background .2s ease; }
tbody tr:hover { background: var(--accent-soft); }
tbody tr:last-child td { border-bottom: none; }

/* Image & Video  */
img, video {
  max-width: 100%;
  height: auto;
  border-radius: var(--radius);
  margin: 1rem 0;
}

/* Metric  */
.metric-card {
  display: inline-flex;
  flex-direction: column;
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1.2rem 1.6rem;
  min-width: 160px;
  box-shadow: var(--shadow);
  transition: transform .2s ease, box-shadow .2s ease;
}
.metric-card:hover { transform: translateY(-2px); box-shadow: var(--shadow-lg); }
.metric-label { font-size: 0.82rem; color: var(--fg-muted); text-transform: uppercase; letter-spacing: 0.06em; font-weight: 600; }
.metric-value { font-size: 2rem; font-weight: 800; letter-spacing: -0.03em; margin: 0.15rem 0; }
.metric-delta { font-size: 0.9rem; font-weight: 600; }

/* Progress bar  */
.progress-wrap { margin: 0.8rem 0; }
.progress-label { font-size: 0.85rem; color: var(--fg-muted); margin-bottom: 0.35rem; display: block; }
.progress-track {
  height: 10px;
  background: var(--border);
  border-radius: 999px;
  overflow: hidden;
}
.progress-fill {
  height: 100%;
  background: var(--gradient-progress);
  border-radius: 999px;
  transition: width 0.6s cubic-bezier(.4,0,.2,1);
}

/* Alert  */
.alert {
  padding: 0.85rem 1.2rem;
  border-radius: var(--radius);
  margin: 0.8rem 0;
  font-weight: 500;
  border-left: 4px solid;
  font-size: 0.93rem;
}
.alert-info    { background: var(--alert-info-bg);    border-color: var(--alert-info-border);    color: var(--alert-info-fg); }
.alert-success { background: var(--alert-success-bg); border-color: var(--alert-success-border); color: var(--alert-success-fg); }
.alert-warning { background: var(--alert-warning-bg); border-color: var(--alert-warning-border); color: var(--alert-warning-fg); }
.alert-error   { background: var(--alert-error-bg);   border-color: var(--alert-error-border);   color: var(--alert-error-fg); }

/* Button  */
.btn {
  display: inline-block;
  background: var(--gradient-accent);
  color: var(--bg);
  border: none;
  border-radius: var(--radius);
  padding: 0.6rem 1.6rem;
  font-family: var(--font);
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  box-shadow: var(--shadow);
  transition: transform .2s ease, box-shadow .2s ease;
}
.btn:hover { transform: translateY(-1px); box-shadow: var(--shadow-lg); }
.btn:active { transform: scale(0.97); }

/* Card  */
.card {
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1.4rem 1.6rem;
  margin: 1rem 0;
  box-shadow: var(--shadow);
  transition: transform .2s ease, box-shadow .2s ease;
}
.card:hover { transform: translateY(-2px); box-shadow: var(--shadow-lg); }
.card-title { font-size: 1.15rem; font-weight: 700; margin-bottom: 0.5rem; }
.card-body  { color: var(--fg-muted); line-height: 1.65; }

/* Navbar  */
.navbar {
  background: var(--bg-surface);
  border-bottom: 1px solid var(--border);
  padding: 0.9rem 24px;
  margin: 0 0 2rem;
  font-family: var(--font);
  box-shadow: var(--shadow);
  width: 100%;
}
.navbar-inner {
  max-width: 860px;
  margin: 0 auto;
  width: 100%;
}
.navbar-brand {
  font-size: 1.15rem;
  font-weight: 800;
  letter-spacing: -0.03em;
  color: var(--fg);
}
.navbar-links {
  display: flex;
  gap: 1.5rem;
  align-items: center;
}
.navbar-links a {
  font-size: 0.88rem;
  font-weight: 500;
  color: var(--fg-muted);
  text-decoration: none;
  transition: color .2s ease;
}
.navbar-links a:hover {
  color: var(--fg);
}
.navbar-links a.active {
  color: var(--accent);
  font-weight: 600;
}

/* simple: logo left, links right */
.navbar-simple .navbar-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

/* centered: logo centered, links below */
.navbar-centered .navbar-inner {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.6rem;
}
.navbar-centered .navbar-brand {
  font-size: 1.3rem;
}

/* Footer  */
.site-footer {
  background: var(--bg-surface);
  border-top: 1px solid var(--border);
  padding: 3rem 24px;
  margin: 4rem 0 0;
  font-family: var(--font);
  font-size: 0.88rem;
  color: var(--fg-muted);
  width: 100%;
}
.footer-inner {
  max-width: 860px;
  margin: 0 auto;
  width: 100%;
}
.footer-links {
  display: flex;
  gap: 1.5rem;
}
.footer-links a {
  color: var(--fg-muted);
  text-decoration: none;
  font-weight: 500;
  transition: color .2s ease;
}
.footer-links a:hover {
  color: var(--fg);
}

/* simple: single line */
.footer-simple .footer-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

/* columns: grid above copyright */
.footer-columns .footer-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 2rem;
  margin-bottom: 1.5rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid var(--border);
}
.footer-col {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.footer-col-heading {
  font-weight: 700;
  font-size: 0.82rem;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--fg);
  margin-bottom: 0.25rem;
}
.footer-col a {
  color: var(--fg-muted);
  text-decoration: none;
  font-size: 0.88rem;
  transition: color .2s ease;
}
.footer-col a:hover {
  color: var(--fg);
}
.footer-bottom {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

/* Theme switcher (floating container)  */
.theme-switcher-floating {
  position: fixed;
  top: 16px;
  right: 16px;
  z-index: 9999;
}

/* Theme dropdown  */
.theme-dropdown {
  position: relative;
  display: inline-block;
}
.theme-dropdown-btn {
  background: transparent;
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 6px 12px;
  font-size: 0.85rem;
  font-weight: 500;
  color: var(--fg-muted);
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all 0.15s ease;
  font-family: var(--font);
}
.theme-dropdown-btn:hover {
  color: var(--fg);
  border-color: var(--fg-muted);
  background: var(--accent-soft);
}
.theme-dropdown-menu {
  position: absolute;
  top: calc(100% + 6px);
  right: 0;
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 4px;
  min-width: 130px;
  box-shadow: var(--shadow-lg);
  display: none;
  flex-direction: column;
  gap: 2px;
  z-index: 10000;
}
.theme-dropdown-menu button {
  background: transparent;
  border: none;
  border-radius: 4px;
  padding: 6px 12px;
  font-size: 0.82rem;
  font-weight: 500;
  color: var(--fg-muted);
  text-align: left;
  cursor: pointer;
  width: 100%;
  transition: all 0.15s ease;
  font-family: var(--font);
}
.theme-dropdown-menu button:hover {
  color: var(--fg);
  background: var(--accent-soft);
}
.theme-dropdown-menu button.active {
  background: var(--accent);
  color: var(--bg);
  font-weight: 600;
}
.theme-dropdown.open .theme-dropdown-menu {
  display: flex;
}
.theme-dropdown.open .chevron {
  transform: rotate(180deg);
}
.theme-dropdown .chevron {
  transition: transform 0.2s ease;
}

/* Accordion  */
.accordion {
  margin: 1rem 0;
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.accordion-item {
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  overflow: hidden;
  transition: box-shadow .2s ease;
}
.accordion-item:hover { box-shadow: var(--shadow); }
.accordion-item[open] { box-shadow: var(--shadow-lg); }
.accordion-summary {
  padding: 0.9rem 1.2rem;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.95rem;
  color: var(--fg);
  display: flex;
  align-items: center;
  justify-content: space-between;
  list-style: none;
  user-select: none;
  transition: background .15s ease;
}
.accordion-summary:hover { background: var(--accent-soft); }
.accordion-summary::-webkit-details-marker { display: none; }
.accordion-chevron {
  transition: transform .25s ease;
  flex-shrink: 0;
  color: var(--fg-muted);
}
.accordion-item[open] .accordion-chevron {
  transform: rotate(180deg);
}
.accordion-content {
  padding: 0 1.2rem 1rem;
  color: var(--fg-muted);
  line-height: 1.65;
  font-size: 0.93rem;
}

/* Tabs  */
.tabs-container {
  margin: 1rem 0;
}
.tab-buttons {
  display: flex;
  gap: 0;
  border-bottom: 2px solid var(--border);
  margin-bottom: 0;
}
.tab-btn {
  background: transparent;
  border: none;
  border-bottom: 2px solid transparent;
  padding: 0.65rem 1.4rem;
  font-family: var(--font);
  font-size: 0.9rem;
  font-weight: 500;
  color: var(--fg-muted);
  cursor: pointer;
  margin-bottom: -2px;
  transition: all .2s ease;
}
.tab-btn:hover {
  color: var(--fg);
  background: var(--accent-soft);
}
.tab-btn.active {
  color: var(--accent);
  border-bottom-color: var(--accent);
  font-weight: 600;
}
.tab-panel {
  padding: 1.2rem 0;
}

/* Link button (anchor styled as .btn)  */
a.btn {
  text-decoration: none;
  color: var(--bg);
}
a.btn:hover {
  opacity: 1;
  text-decoration: none;
}

/* Page transitions  */
.pyclay-page {
  animation: pcFadeIn 0.25s ease;
}
@keyframes pcFadeIn {
  from { opacity: 0; transform: translateY(6px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* Mobile hamburger  */
.navbar-toggle {
  display: none;
  background: transparent;
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 6px 8px;
  cursor: pointer;
  color: var(--fg-muted);
  transition: all .15s ease;
}
.navbar-toggle:hover {
  color: var(--fg);
  background: var(--accent-soft);
}

/* Responsive breakpoint  */
@media (max-width: 768px) {
  /* Stack grid columns vertically  */
  [style*="grid-template-columns"] {
    grid-template-columns: 1fr !important;
  }

  /* Stack navbar links vertically  */
  .navbar-simple .navbar-inner {
    flex-wrap: wrap;
  }
  .navbar-toggle { display: block; }
  .navbar-links {
    display: none;
    flex-direction: column;
    width: 100%;
    gap: 0.5rem;
    padding-top: 0.75rem;
    border-top: 1px solid var(--border);
    margin-top: 0.75rem;
  }
  .navbar-links.open {
    display: flex;
  }

  /* Footer responsive  */
  .footer-simple .footer-inner,
  .footer-bottom {
    flex-direction: column;
    gap: 0.75rem;
    text-align: center;
  }
  .footer-links { justify-content: center; }

  /* Content wrapper padding  */
  .content-wrapper {
    padding: 32px 16px 60px;
  }
}
"""


# Fonts per theme family
_FONT_LINKS = {
    "original": (
        '<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">'
    ),
    "vercel": (
        '<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">'
    ),
}

_FONT_STACKS = {
    "original": {
        "font": "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
        "mono": "'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace",
    },
    "vercel": {
        "font": "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
        "mono": "'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace",
    },
}


# Hot-reload script
_HOT_RELOAD_JS = r"""
<script>
  let _pc_last = null;
  setInterval(async () => {
    try {
      const res = await fetch("/poll");
      const ts  = await res.text();
      if (_pc_last === null) { _pc_last = ts; return; }
      if (ts !== _pc_last) { location.reload(); }
    } catch(e) {}
  }, 800);
</script>
"""

# Theme switcher JS
_THEME_SWITCHER_JS = """
<script>
(function() {
  const THEMES = %THEMES_JSON%;
  const root = document.documentElement;
  const labels = { ivory: 'Ivory', nebula: 'Nebula', arctic: 'Arctic', obsidian: 'Obsidian' };

  function applyTheme(name) {
    root.setAttribute('data-theme', name);
    // Update active state in dropdowns
    document.querySelectorAll('.theme-dropdown-menu button').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.theme === name);
    });
    // Update button text in all dropdowns
    document.querySelectorAll('.theme-dropdown-btn span').forEach(span => {
      span.textContent = labels[name] || 'Theme';
    });
    localStorage.setItem('pyclay-theme', name);
  }

  // Restore saved theme on root ASAP to prevent FOUC
  const saved = localStorage.getItem('pyclay-theme');
  if (saved && THEMES.includes(saved)) {
    root.setAttribute('data-theme', saved);
  }

  function init() {
    // Sync dropdown UI with current theme on load
    const currentTheme = root.getAttribute('data-theme');
    if (currentTheme) {
      document.querySelectorAll('.theme-dropdown-menu button').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.theme === currentTheme);
      });
      document.querySelectorAll('.theme-dropdown-btn span').forEach(span => {
        span.textContent = labels[currentTheme] || 'Theme';
      });
    }

    // Toggle dropdown on button click
    document.addEventListener('click', (e) => {
      const btn = e.target.closest('.theme-dropdown-btn');
      if (btn) {
        e.stopPropagation();
        const dropdown = btn.closest('.theme-dropdown');
        if (dropdown) {
          const wasOpen = dropdown.classList.contains('open');
          document.querySelectorAll('.theme-dropdown').forEach(d => d.classList.remove('open'));
          if (!wasOpen) {
            dropdown.classList.add('open');
          }
        }
      } else {
        // Close all dropdowns when clicking outside
        document.querySelectorAll('.theme-dropdown').forEach(dropdown => {
          dropdown.classList.remove('open');
        });
      }
    });

    // Theme selector click handlers
    document.querySelectorAll('.theme-dropdown-menu button').forEach(btn => {
      btn.addEventListener('click', () => {
        applyTheme(btn.dataset.theme);
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
</script>
"""


def _build_theme_dropdown_html(current_theme):
    """Build the theme selector dropdown."""
    labels = {
        "ivory": "Ivory",
        "nebula": "Nebula",
        "arctic": "Arctic",
        "obsidian": "Obsidian",
    }
    buttons = []
    for key, label in labels.items():
        active = " active" if key == current_theme else ""
        buttons.append(f'<button class="{active.strip()}" data-theme="{key}">{label}</button>')
    
    current_label = labels.get(current_theme, "Theme")
    
    return f"""<div class="theme-dropdown">
  <button class="theme-dropdown-btn" aria-haspopup="true" aria-expanded="false">
    <span>{current_label}</span>
    <svg class="chevron" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"></polyline></svg>
  </button>
  <div class="theme-dropdown-menu">
    {"".join(buttons)}
  </div>
</div>"""


_ROUTER_JS = """
<script>
(function() {
  function navigate() {
    const hash = window.location.hash.substring(1);
    const pages = document.querySelectorAll('.pyclay-page');
    let found = false;
    let activePageName = '';

    pages.forEach((p, idx) => {
      const name = p.dataset.pageName || '';
      const isMatch = name.toLowerCase() === hash.toLowerCase() || p.id.toLowerCase() === ('page-' + hash).toLowerCase();
      if (isMatch || (!hash && idx === 0)) {
        p.style.display = 'block';
        found = true;
        activePageName = name;
      } else {
        p.style.display = 'none';
      }
    });

    if (!found && pages.length > 0) {
      pages.forEach((p, idx) => {
        p.style.display = idx === 0 ? 'block' : 'none';
      });
      activePageName = pages[0].dataset.pageName || '';
    }

    // Update active state on navbar links
    document.querySelectorAll('.navbar-links a').forEach(a => {
      const href = a.getAttribute('href') || '';
      if (href.startsWith('#')) {
        const pageHash = href.substring(1).toLowerCase();
        const currentHash = (hash || activePageName).toLowerCase();
        a.classList.toggle('active', pageHash === currentHash);
      } else {
        a.classList.remove('active');
      }
    });

    // Scroll to top of the page on navigation
    window.scrollTo(0, 0);
  }

  window.addEventListener('hashchange', navigate);
  window.addEventListener('load', navigate);
})();
</script>
"""


_TABS_JS = """
<script>
document.addEventListener('DOMContentLoaded', () => {
  document.addEventListener('click', (e) => {
    const btn = e.target.closest('.tab-btn');
    if (!btn) return;
    const group = btn.dataset.tabGroup;
    const idx = btn.dataset.tabIdx;
    // Update buttons
    document.querySelectorAll(`.tab-btn[data-tab-group="${group}"]`).forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    // Update panels
    document.querySelectorAll(`.tab-panel[data-tab-group="${group}"]`).forEach(p => {
      p.style.display = p.dataset.tabPanel === idx ? 'block' : 'none';
    });
  });
});
</script>
"""


_HAMBURGER_JS = """
<script>
document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.querySelector('.navbar-toggle');
  const links = document.querySelector('.navbar-links');
  if (toggle && links) {
    toggle.addEventListener('click', () => {
      links.classList.toggle('open');
    });
  }
});
</script>
"""


# Full page
def render_page(title=None):
    global _tab_id_counter
    _tab_id_counter = 0  # Reset for deterministic IDs across hot reloads

    config = _runtime.get_page_config()
    page_title = title or config.get("title", "My App")
    theme = config.get("theme", "ivory")
    favicon = config.get("favicon", "")
    custom_css = config.get("custom_css", "")

    import os
    if not favicon and os.path.exists(os.path.join("assets", "favicon.ico")):
        favicon = "assets/favicon.ico"

    # Extract all pages
    pages = _runtime.get_pages()

    # Find global navbar & footer in any page tree
    navbars = []
    footers = []
    for page_tree in pages.values():
        for c in page_tree:
            if c["type"] == "navbar":
                navbars.append(c)
            elif c["type"] == "footer":
                footers.append(c)

    navbar_html = render_component(navbars[0]) if navbars else ""
    footer_html = render_component(footers[0]) if footers else ""

    # Render each page hidden or block, excluding nav/footer components
    pages_html = []
    for page_name, page_tree in pages.items():
        page_children = []
        for c in page_tree:
            if c["type"] not in ("navbar", "footer"):
                page_children.append(render_component(c))

        if page_children or len(pages) == 1:
            page_content = "\n".join(page_children)
            wrapper_html = f'<div class="content-wrapper">{page_content}</div>'
            pages_html.append(
                f'<div id="page-{_esc(page_name)}" class="pyclay-page" data-page-name="{_esc(page_name)}" style="display: none;">'
                f'{wrapper_html}'
                f'</div>'
            )

    body = "\n".join([navbar_html] + pages_html + [footer_html])
    favicon_tag = ""
    if favicon:
        if favicon.endswith(".ico"):
            favicon_tag = f'<link rel="icon" type="image/x-icon" href="{_esc(favicon)}">'
        elif favicon.endswith(".png"):
            favicon_tag = f'<link rel="icon" type="image/png" href="{_esc(favicon)}">'
        else:
            favicon_tag = f'<link rel="icon" href="{_esc(favicon)}">'
    custom_css_tag = f'<link rel="stylesheet" href="{_esc(custom_css)}">' if custom_css else ""

    # Determine font family
    font_family = "vercel" if theme in ("arctic", "obsidian") else "original"
    font_links = _FONT_LINKS[font_family]
    font_stack = _FONT_STACKS[font_family]

    # Build all theme CSS blocks with [data-theme="..."] selectors
    theme_css_blocks = []
    for theme_name, vars_css in _THEME_VARS.items():
        theme_css_blocks.append(f'[data-theme="{theme_name}"] {{ {vars_css} }}')
    all_theme_css = "\n".join(theme_css_blocks)

    # Theme switcher
    theme_switcher = config.get("theme_switcher", True)
    has_navbar = len(navbars) > 0
    if has_navbar or not theme_switcher:
        switcher_html = ""
    else:
        switcher_html = f'<div class="theme-switcher-floating">{_build_theme_dropdown_html(theme)}</div>'

    if theme_switcher:
        switcher_js = _THEME_SWITCHER_JS.replace(
            "%THEMES_JSON%",
            '["ivory","nebula","arctic","obsidian"]'
        )
    else:
        switcher_js = ""

    # Prism.js syntax highlighting (lightweight, no build step)
    prism_theme_light = 'prism'
    prism_css = f'<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/{prism_theme_light}.min.css">'
    prism_js = (
        '<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>'
        '<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-python.min.js"></script>'
        '<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-bash.min.js"></script>'
        '<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-javascript.min.js"></script>'
        '<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-css.min.js"></script>'
    )
    # Override Prism styles to match pyclay themes
    prism_override_css = """
    /* Override Prism.js to use pyclay theme tokens  */
    pre[class*="language-"], code[class*="language-"] {
      background: transparent !important;
      text-shadow: none !important;
      color: var(--fg) !important;
      font-family: var(--mono) !important;
      font-size: 0.9em !important;
    }
    .token.comment, .token.prolog, .token.doctype, .token.cdata { color: var(--fg-muted) !important; }
    .token.keyword { color: var(--accent) !important; font-weight: 600; }
    .token.string, .token.attr-value { color: #10b981 !important; }
    .token.number { color: #f59e0b !important; }
    .token.function { color: #3b82f6 !important; }
    .token.operator { color: var(--fg-muted) !important; background: transparent !important; }
    .token.builtin, .token.class-name { color: #8b5cf6 !important; }
    .token.punctuation { color: var(--fg-muted) !important; }
    .token.boolean { color: #ef4444 !important; }
    .token.decorator, .token.atrule { color: #f59e0b !important; }
    """

    return f"""<!DOCTYPE html>
<html lang="en" data-theme="{_esc(theme)}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{_esc(page_title)}</title>
  {favicon_tag}
  {font_links}
  {_FONT_LINKS["original"]}
  {prism_css}
  <style>
    :root {{
      --font: {font_stack["font"]};
      --mono: {font_stack["mono"]};
    }}
    {all_theme_css}
    {_BASE_CSS}
    {prism_override_css}
  </style>
  {custom_css_tag}
  {_HOT_RELOAD_JS}
  {switcher_js}
  {_ROUTER_JS}
  {_TABS_JS}
  {_HAMBURGER_JS}
</head>
<body>
{switcher_html}
{body}
{prism_js}
<script>if (typeof Prism !== 'undefined') Prism.highlightAll();</script>
</body>
</html>"""
