<p align="center">
  <h1 align="center">pyclay</h1>
  <p align="center"><strong>Build beautiful, responsive web pages entirely in Python.</strong></p>
  <p align="center">No HTML. No CSS. No JavaScript. Just Python.</p>
</p>

<p align="center">
  <a href="https://pypi.org/project/pyclay/"><img src="https://img.shields.io/pypi/v/pyclay?color=6366f1&style=flat-square" alt="PyPI"></a>
  <a href="https://pypi.org/project/pyclay/"><img src="https://img.shields.io/pypi/pyversions/pyclay?color=818cf8&style=flat-square" alt="Python"></a>
  <a href="LICENSE"><img src="https://img.shields.io/github/license/ayush-sharma11/pyclay?color=10b981&style=flat-square" alt="License"></a>
</p>

---

pyclay is a Python-native static site builder. Write Python functions, get a production-ready HTML page - with themes, responsive layouts, and zero frontend knowledge required.

## Features

- **4 Built-in Themes** - Ivory, Nebula, Arctic, and Obsidian. Switch live via dropdown.
- **Fully Responsive** - Columns stack on mobile, navbar collapses to hamburger.
- **Hot Reload** - Edit Python, save, browser refreshes instantly.
- **Static Export** - `pyclay build app.py` → one HTML file. Deploy anywhere.
- **Rich Components** - Cards, tables, metrics, accordions, tabs, alerts, code blocks with syntax highlighting, and more.
- **Zero Config** - No `package.json`, no `webpack`, no `node_modules`. Just `pip install` and go.

## Quick Start

```bash
pip install pyclay
```

Create `app.py`:

```python
import pyclay as pc

pc.page_config(title="My Site", theme="obsidian")
pc.navbar("My Site", links=[
    {"text": "Home", "href": "#home"},
    {"text": "About", "href": "#about"},
])

pc.page("Home")
pc.heading("Hello World!")
pc.text("Built with pyclay - no HTML required.")

pc.card(title="Why pyclay?",
        body="Because life is too short to write HTML.")

pc.page("About")
pc.text("This is the about page.")
```

Run the dev server:

```bash
pyclay run app.py
```

Build for production:

```bash
pyclay build app.py
# → dist/index.html (deploy to GitHub Pages, Netlify, etc.)
```

## Components

| Component | Usage |
|-----------|-------|
| **Typography** | `pc.heading()`, `pc.text()`, `pc.blockquote()` |
| **Layout** | `pc.columns()`, `pc.column()`, `pc.container()` |
| **Data** | `pc.table()`, `pc.metric()`, `pc.progress_bar()` |
| **UI** | `pc.card()`, `pc.button()`, `pc.link_button()`, `pc.badge()`, `pc.alert()` |
| **Interactive** | `pc.accordion()`, `pc.tabs()`, `pc.tab_panel()` |
| **Media** | `pc.image()`, `pc.video()`, `pc.code_block()`, `pc.link()` |
| **Navigation** | `pc.navbar()`, `pc.footer()`, `pc.page()` |
| **Utility** | `pc.spacer()`, `pc.divider()`, `pc.html_raw()` |

## Static Assets & Favicon

Place all your static files (images, videos, etc.) inside an `assets/` folder in your project root. You can reference them in your python code using relative paths like `assets/...`.

* **Favicon:** If you put `favicon.ico` in your `assets/` folder, `pyclay` will automatically detect and link it as your page favicon.
* **Dev Server:** The dev server (`pyclay run`) automatically serves static files requested from your `assets/` folder.
* **Static Export:** The build command (`pyclay build`) copies the entire `assets/` folder into your output directory (`dist/assets/`), keeping all media links fully working when deployed.

## Themes

```python
pc.page_config(
    theme="obsidian",      # ivory | nebula | arctic | obsidian
    theme_switcher=True    # set to False to lock the site to one theme and hide the toggle
)
```

By default, users can switch themes live via the built-in dropdown in the navbar (or floating). If you set `theme_switcher=False`, the site will remain locked to the chosen theme and no toggle dropdown elements will be rendered.

## Layout System

```python
with pc.columns([1, 2], gap="2rem"):
    with pc.column():
        pc.text("Narrow column")
    with pc.column():
        pc.text("Wide column")
```

Columns automatically stack vertically on mobile (<768px).

## CLI Reference

| Command | Description |
|---------|-------------|
| `pyclay run <file.py>` | Start dev server with hot reload |
| `pyclay run <file.py> --port 3000` | Use a custom port |
| `pyclay build <file.py>` | Export static HTML to `dist/` |
| `pyclay build <file.py> --out public` | Custom output directory |

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

Apache 2.0 - see [LICENSE](LICENSE).
