# examples/app.py  --  pyclay showcase & documentation
import pyclay as pc

# Page config
pc.page_config(title="pyclay - Python to Web", theme="obsidian")

# Global Navbar
pc.navbar("pyclay", links=[
    {"text": "Home", "href": "#home"},
    {"text": "Docs", "href": "#docs"},
    {"text": "Components", "href": "#components"},
], variant="simple")


# =========================================================================
#  PAGE: HOME
# =========================================================================
pc.page("Home")

pc.heading("pyclay", style={"text_align": "center", "font_size": "3.5rem",
    "margin_top": "3rem", "margin_bottom": "0.2rem"})

pc.text("Build beautiful, responsive web pages entirely in Python.", style={
    "text_align": "center", "font_size": "1.25rem", "color": "var(--fg-muted)", "margin_bottom": "1.5rem"})

with pc.columns([1, 1], gap="1rem", style={"max_width": "350px", "margin": "0 auto"}):
    with pc.column():
        pc.link_button("Get Started", "#docs", style={"width": "100%", "text_align": "center"})
    with pc.column():
        pc.link_button("GitHub", "https://github.com/ayush-sharma11/pyclay", style={"width": "100%", "text_align": "center", "background": "transparent", "border": "1px solid var(--border)", "color": "var(--fg)"})

pc.spacer("3rem")

# Hero Code Block
pc.heading("Quick Start", level=3, style={"text_align": "center"})
pc.code_block("""# app.py
import pyclay as pc

# Define pages programmatically
pc.page_config(
    title="My Site", 
    theme="obsidian",
    theme_switcher=True  # Set to False to lock the theme and hide the switcher dropdown
)
pc.navbar("My Site")

pc.page("Home")
pc.heading("Hello World!")
pc.text("Powered by pyclay.")

pc.page("About")
pc.text("This is the about page.")
""", language="python")

pc.spacer("4rem")

# Features
pc.heading("Features", level=2, style={"border_bottom": "1px solid var(--border)", "padding_bottom": "0.5rem"})
pc.spacer("1rem")

with pc.columns([1, 1], gap="1.5rem"):
    with pc.column():
        pc.card(title="4 Creative Themes",
                body="Switch between Ivory, Nebula, Arctic, and Obsidian live with the navbar dropdown. Zero CSS knowledge required.")
    with pc.column():
        pc.card(title="Hot Reloading",
                body="Edit your python file, save, and watch the page refresh instantly in the browser.")

with pc.columns([1, 1], gap="1.5rem"):
    with pc.column():
        pc.card(title="Responsive Grid Layout",
                body="Columns automatically stack vertically on mobile. Arrange components side-by-side with columns() and container() context managers.")
    with pc.column():
        pc.card(title="Static Export",
                body="Build production-ready HTML with `pyclay build app.py`. Deploy anywhere - GitHub Pages, Netlify, or any static host.")

pc.footer(
    text="© 2026 pyclay. Open source under Apache-2.0 License.",
    variant="simple",
    links=[
        {"text": "GitHub", "href": "https://github.com/ayush-sharma11/pyclay"},
    ]
)
