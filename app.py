# app.py  --  pyclay showcase & documentation
import datetime
import pyclay as pc

# Page config
pc.page_config(title="pyclay - Python to Web", theme="obsidian")

# Global Navbar
# The navbar links use hash routing matching the page names defined below.
pc.navbar("pyclay", links=[
    {"text": "Home", "href": "#home"},
    {"text": "Features", "href": "#features"},
    {"text": "Tutorial", "href": "#tutorial"},
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

with pc.columns([1, 1, 1], gap="1rem", style={"max_width": "480px", "margin": "0 auto"}):
    with pc.column():
        pc.link_button("Get Started", "#docs", style={"width": "100%", "text_align": "center"})
    with pc.column():
        pc.link_button("GitHub", "https://github.com/ayush-sharma11/pyclay", style={"width": "100%", "text_align": "center", "background": "transparent", "border": "1px solid var(--border)", "color": "var(--fg)"})
    with pc.column():
        pc.link_button("PyPI", "https://pypi.org/project/pyclay/", style={"width": "100%", "text_align": "center", "background": "transparent", "border": "1px solid var(--border)", "color": "var(--fg)"})

pc.spacer("3rem")

# Hero Code Block
pc.heading("Quick Start", level=3, style={"text_align": "center"})
pc.code_block("""# app.py
import pyclay as pc

# Define pages programmatically
pc.page_config(title="My Site", theme="obsidian")
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

with pc.columns([1, 1], gap="1.5rem"):
    with pc.column():
        pc.card(title="Syntax Highlighting",
                body="Code blocks are automatically syntax-highlighted for Python, Bash, JS, and CSS using Prism.js - themed to match your selected palette.")
    with pc.column():
        pc.card(title="Custom Styling",
                body="Every single function accepts a style dict to override padding, margins, colors, borders, and more.")


# =========================================================================
#  PAGE: FEATURES
# =========================================================================
pc.page("Features")

pc.heading("Core Features", level=2, style={"border_bottom": "1px solid var(--border)", "padding_bottom": "0.5rem"})
pc.spacer("1.5rem")

pc.text("pyclay comes packed with features designed to build performant, beautiful static sites in pure Python with zero build configuration.")

pc.spacer("1.5rem")

# Row 1 of Features
with pc.columns([1, 1], gap="1.5rem"):
    with pc.column():
        pc.card(title="4 Creative Themes",
                body="Switch between Ivory, Nebula, Arctic, and Obsidian live with the built-in dropdown, or lock your site to a single theme.")
    with pc.column():
        pc.card(title="Responsive Grid Layout",
                body="Columns automatically stack vertically on mobile. Flexibly arrange components using the `columns()` and `container()` context managers.")

pc.spacer("1.5rem")

# Row 2 of Features
with pc.columns([1, 1], gap="1.5rem"):
    with pc.column():
        pc.card(title="Hot Reloading",
                body="Edit your python code, save, and watch the page refresh instantly in the browser in real-time.")
    with pc.column():
        pc.card(title="Zero-JS Static Export",
                body="Build and export standalone, lightweight HTML files with `pyclay build`. Perfect for GitHub Pages, Netlify, Vercel, or custom servers.")

pc.spacer("1.5rem")

# Row 3 of Features
with pc.columns([1, 1], gap="1.5rem"):
    with pc.column():
        pc.card(title="Syntax Highlighting",
                body="Automatic, themed syntax highlighting for Python, Bash, JS, and CSS using Prism.js out-of-the-box.")
    with pc.column():
        pc.card(title="Custom Styling Control",
                body="Override styles dynamically. Every component accepts a `style` dictionary to adjust margins, colors, borders, and alignments.")


# =========================================================================
#  PAGE: TUTORIAL
# =========================================================================
pc.page("Tutorial")

pc.heading("Tutorial: Build Your First Site", level=2, style={"border_bottom": "1px solid var(--border)", "padding_bottom": "0.5rem"})
pc.spacer("1.5rem")

pc.text("Follow this step-by-step guide to create, run, and export a multi-page pyclay site in under 5 minutes.")

pc.spacer("1.5rem")

pc.heading("Step 1: Install Pyclay", level=3)
pc.text("Open your terminal and install the library via pip (also hosted on [PyPI](https://pypi.org/project/pyclay/)):")
pc.code_block("pip install pyclay", language="bash")

pc.spacer("1.5rem")

pc.heading("Step 2: Create your App Code", level=3)
pc.text("Create a file named `app.py` and write your pages programmatically in pure Python:")
pc.code_block("""import pyclay as pc

# Configure the tab title and page theme
pc.page_config(title="My First App", theme="nebula")

# Add a header navigation bar
pc.navbar("My Brand", links=[
    {"text": "Home", "href": "#home"},
    {"text": "About", "href": "#about"}
])

# Define the Home page
pc.page("Home")
pc.heading("Welcome to My Site!")
pc.text("This site is built entirely in Python using pyclay.")
pc.button("Get Started")

# Define the About page
pc.page("About")
pc.heading("About Us")
pc.text("We write Python codes that convert to static web pages.")
""", language="python")

pc.spacer("1.5rem")

pc.heading("Step 3: Run the Development Server", level=3)
pc.text("Launch the dev server with hot-reload enabled. Your browser will open the page automatically:")
pc.code_block("pyclay run app.py", language="bash")
pc.text("Try modifying the text in your `app.py` file and saving it - the browser will refresh instantly to show the changes!")

pc.spacer("1.5rem")

pc.heading("Step 4: Build for Production", level=3)
pc.text("When you are ready to deploy, export your site to optimized static HTML:")
pc.code_block("pyclay build app.py --out dist", language="bash")
pc.text("This creates a standalone `dist/index.html` file alongside your static assets that you can upload to any static host like GitHub Pages, Netlify, or Vercel.")


# =========================================================================
#  PAGE: DOCS
# =========================================================================
pc.page("Docs")

pc.heading("Docs & Getting Started", level=2, style={"border_bottom": "1px solid var(--border)", "padding_bottom": "0.5rem"})
pc.spacer("1.5rem")

pc.heading("Installation", level=3)
pc.text("Install the library from pip in your terminal (or view the package on [PyPI](https://pypi.org/project/pyclay/)):")
pc.code_block("pip install pyclay", language="bash")

pc.spacer("1rem")

pc.heading("CLI Commands", level=3)
pc.text("Run your pyclay application using the built-in CLI watcher, which automatically watches your code for changes and hot-reloads the browser:")
pc.code_block("pyclay run app.py", language="bash")

pc.spacer("1rem")

pc.heading("Static Export", level=3)
pc.text("Build a production-ready HTML file for deployment. The hot-reload script is automatically stripped:")
pc.code_block("pyclay build app.py --out dist", language="bash")

pc.heading("Page Configuration", level=3)
pc.text("Define the page title, initial theme, and optional favicon at the very top of your script. If you place `favicon.ico` in the `assets/` folder, pyclay will automatically detect and use it without manual configuration:")
pc.code_block("""pc.page_config(
    title="My App Title",
    theme="ivory",  # Options: ivory, nebula, arctic, obsidian
    favicon="assets/favicon.ico",  # Optional: defaults to assets/favicon.ico if exists
    theme_switcher=True  # Set to False to lock the theme and hide the switcher dropdown
)""", language="python")

pc.spacer("1.5rem")

pc.heading("Creating Pages", level=3)
pc.text("To enable multi-page apps, call the `page()` function. All elements declared below a `page()` call will belong to that page:")
pc.code_block("""# Page context declarations
pc.page("Home")
pc.text("Home content goes here...")

pc.page("Docs")
pc.text("Docs content goes here...")
""", language="python")


# =========================================================================
#  PAGE: COMPONENTS
# =========================================================================
pc.page("Components")

pc.heading("Components Reference", level=2, style={"border_bottom": "1px solid var(--border)", "padding_bottom": "0.5rem"})
pc.text("Every core component built into pyclay, shown side-by-side with its Python code.", style={"color": "var(--fg-muted)"})
pc.spacer("2rem")

# Component 1: Heading & Text
pc.heading("1. Typography", level=3)
with pc.columns([1, 1], gap="2rem"):
    with pc.column():
        pc.heading("Heading 1", level=1)
        pc.heading("Heading 3", level=3)
        pc.text("This is standard text. You can also make it **bold** or *italic* as inline elements.")
        pc.blockquote("This is a blockquote element for callouts and quotes.")
        pc.text("Press `Ctrl + S` to save.")
    with pc.column():
        pc.code_block("""pc.heading("Heading 1", level=1)
pc.heading("Heading 3", level=3)
pc.text("This is standard text. You can also make it **bold** or *italic* as inline elements.")
pc.blockquote("This is a blockquote element for callouts and quotes.")
pc.text("Press `Ctrl + S` to save.")""", language="python")

pc.spacer("2.5rem")

# Component 2: Lists
pc.heading("2. Lists", level=3)
with pc.columns([1, 1], gap="2rem"):
    with pc.column():
        pc.bullet_list(["Unordered item A", "Unordered item B", "Unordered item C"])
        pc.ordered_list(["First step", "Second step", "Third step"])
    with pc.column():
        pc.code_block("""pc.bullet_list([
    "Unordered item A",
    "Unordered item B",
    "Unordered item C"
])
pc.ordered_list([
    "First step",
    "Second step",
    "Third step"
])""", language="python")

pc.spacer("2.5rem")

# Component 3: Badges & Buttons
pc.heading("3. Badges, Buttons & Alerts", level=3)
with pc.columns([1, 1], gap="2rem"):
    with pc.column():
        pc.badge("Beta Version", color="#f59e0b")
        pc.badge("New Feature", color="#10b981")
        pc.spacer("0.5rem")
        pc.button("Primary Button")
        pc.button("Accent Button", style={"background": "linear-gradient(135deg, #10b981, #059669)", "margin_left": "0.5rem"})
        pc.spacer("0.5rem")
        pc.alert("Successful operation alert box.", variant="success")
        pc.alert("Warning message alert box.", variant="warning")
        pc.alert("Error failure alert box.", variant="error")
    with pc.column():
        pc.code_block("""pc.badge("Beta Version", color="#f59e0b")
pc.button("Primary Button")
pc.alert("Successful operation...",
         variant="success")
pc.alert("Warning message...",
         variant="warning")""", language="python")

pc.spacer("2.5rem")

# Component 4: Metric Cards
pc.heading("4. Metrics", level=3)
with pc.columns([1, 1], gap="2rem"):
    with pc.column():
        pc.metric("Conversion Rate", "3.42%", delta="+0.8%", delta_color="green")
        pc.spacer("0.5rem")
        pc.metric("Bounce Rate", "42.1%", delta="-1.5%", delta_color="red")
    with pc.column():
        pc.code_block("""pc.metric(
    "Conversion Rate",
    "3.42%",
    delta="+0.8%",
    delta_color="green"
)
pc.metric(
    "Bounce Rate",
    "42.1%",
    delta="-1.5%",
    delta_color="red"
)""", language="python")

pc.spacer("2.5rem")

# Component 5: Progress Bar
pc.heading("5. Progress Bars", level=3)
with pc.columns([1, 1], gap="2rem"):
    with pc.column():
        pc.progress_bar(78, label="Project Milestones")
        pc.spacer("0.5rem")
        pc.progress_bar(42, label="Tasks Done")
    with pc.column():
        pc.code_block("""pc.progress_bar(
    78,
    label="Project Milestones"
)""", language="python")

pc.spacer("2.5rem")

# Component 6: Table
pc.heading("6. Data Tables", level=3)
with pc.columns([1, 1], gap="2rem"):
    with pc.column():
        pc.table(
            headers=["Language", "Typing", "Popularity"],
            rows=[
                ["Python", "Dynamic", "5 / 5"],
                ["Rust", "Static", "4 / 5"],
                ["Go", "Static", "4 / 5"]
            ]
        )
    with pc.column():
        pc.code_block("""pc.table(
    headers=["Language", "Typing", "Popularity"],
    rows=[
        ["Python", "Dynamic", "5 / 5"],
        ["Rust", "Static", "4 / 5"],
        ["Go", "Static", "4 / 5"]
    ]
)""", language="python")

pc.spacer("2.5rem")

# Component 7: Custom Containers & Columns
pc.heading("7. Layout Columns & Containers", level=3)
with pc.columns([1, 1], gap="2rem"):
    with pc.column():
        with pc.container(style={
            "background": "var(--accent-soft)",
            "padding": "1.5rem",
            "border_radius": "8px",
            "border": "1px solid var(--border)"
        }):
            pc.heading("Inside Container", level=4, style={"margin_top": "0"})
            pc.text("This is grouped inside a styled container element.")
    with pc.column():
        pc.code_block("""with pc.container(style={
    "background": "var(--accent-soft)",
    "padding": "1.5rem",
    "border_radius": "8px"
}):
    pc.heading("Inside Container", level=4)
    pc.text("This is grouped...")""", language="python")

pc.spacer("2.5rem")

# Component 8: Accordion
pc.heading("8. Accordion", level=3)
with pc.columns([1, 1], gap="2rem"):
    with pc.column():
        pc.accordion([
            {"title": "What is pyclay?", "content": "pyclay is a Python library that lets you build beautiful, responsive static websites entirely in Python - no HTML, CSS, or JS knowledge needed."},
            {"title": "How does hot reload work?", "content": "The dev server watches your Python file for changes. When you save, it re-executes your script and pushes the new HTML to the browser automatically."},
            {"title": "Can I deploy the output?", "content": "Yes! Run `pyclay build app.py` to export a standalone index.html file. Deploy it to GitHub Pages, Netlify, Vercel, or any static host."},
        ])
    with pc.column():
        pc.code_block("""pc.accordion([
    {"title": "What is pyclay?",
     "content": "pyclay is a Python..."},
    {"title": "How does hot reload work?",
     "content": "The dev server watches..."},
    {"title": "Can I deploy the output?",
     "content": "Yes! Run pyclay build..."},
])""", language="python")

pc.spacer("2.5rem")

# Component 9: Tabs
pc.heading("9. Tabs", level=3)
with pc.columns([1, 1], gap="2rem"):
    with pc.column():
        pc.tabs(["Overview", "Installation", "Usage"])
        with pc.tab_panel():
            pc.text("pyclay turns Python scripts into polished web pages with zero frontend knowledge.")
        with pc.tab_panel():
            pc.code_block("pip install pyclay", language="bash")
        with pc.tab_panel():
            pc.code_block("pyclay run app.py", language="bash")
    with pc.column():
        pc.code_block("""pc.tabs(["Overview", "Install", "Usage"])
with pc.tab_panel():
    pc.text("Overview content...")
with pc.tab_panel():
    pc.code_block("pip install pyclay")
with pc.tab_panel():
    pc.code_block("pyclay run app.py")""", language="python")

pc.spacer("2.5rem")

# Component 10: Link Button
pc.heading("10. Link Button", level=3)
with pc.columns([1, 1], gap="2rem"):
    with pc.column():
        pc.link_button("Go to Docs", "#docs")
        pc.link_button("GitHub", "#", style={
            "background": "transparent",
            "border": "1px solid var(--border)",
            "color": "var(--fg)",
            "margin_left": "0.5rem"
        })
    with pc.column():
        pc.code_block("""pc.link_button("Go to Docs", "#docs")
pc.link_button("GitHub", "#", style={
    "background": "transparent",
    "border": "1px solid var(--border)",
    "color": "var(--fg)"
})""", language="python")

pc.spacer("2.5rem")

# Component 11: Media (Image & Video)
pc.heading("11. Media (Images & Videos)", level=3)
with pc.columns([1, 1], gap="2rem"):
    with pc.column():
        pc.text("Pyclay supports embedding local or remote images and videos. Place your local files in the `assets/` folder and reference them using `assets/...`.")
        pc.spacer("0.5rem")
        pc.image("assets/test.jpeg", alt="Test Image", width=200)
    with pc.column():
        pc.code_block("""# Render an image with custom width
pc.image("assets/test.jpeg", alt="Test Image", width=200)

# Render a video with custom width
pc.video("assets/test.mp4", controls=True, autoplay=False, width=200)""", language="python")

pc.spacer("2.5rem")

# Component 12: Theme Switcher
pc.heading("12. Theme Switcher Configuration", level=3)
with pc.columns([1, 1], gap="2rem"):
    with pc.column():
        pc.text("You can enable or disable the live theme switcher dropdown in the navbar (or floating toggle). Set `theme_switcher=False` to lock the website to your chosen theme and hide all theme-toggle elements.")
        pc.alert("By default, theme_switcher is set to True.", variant="info")
    with pc.column():
        pc.code_block("""pc.page_config(
    title="My Site",
    theme="nebula",
    theme_switcher=False  # Hide toggle dropdown
)""", language="python")

# =========================================================================
#  PAGE: PRIVACY
# =========================================================================
pc.page("Privacy")

pc.heading("Privacy Policy", level=2, style={"border_bottom": "1px solid var(--border)", "padding_bottom": "0.5rem"})
pc.spacer("1.5rem")
pc.text("Last updated: June 03, 2026")
pc.text("At pyclay, we are committed to protecting your privacy. This Privacy Policy describes how we handle any information when you use our website or open-source software.")

pc.heading("1. Information Collection", level=3)
pc.text("Because pyclay is a static web page builder that runs entirely locally on your machine, **we do not collect, store, or transmit any personal data**.")

pc.heading("2. Local Storage", level=3)
pc.text("Our theme switcher utilizes browser `localStorage` locally on your device to persist your preferred theme selection (Ivory, Nebula, Arctic, or Obsidian). This data never leaves your browser.")

pc.heading("3. Third-party Links", level=3)
pc.text("Our documentation may link to third-party repositories or web pages (like GitHub or Discord). We are not responsible for the privacy practices of those external sites.")


# =========================================================================
#  PAGE: TERMS
# =========================================================================
pc.page("Terms")

pc.heading("Terms of Service", level=2, style={"border_bottom": "1px solid var(--border)", "padding_bottom": "0.5rem"})
pc.spacer("1.5rem")
pc.text("Last updated: June 03, 2026")
pc.text("By accessing or using the pyclay library, CLI, or documentation site, you agree to comply with and be bound by the following Terms of Service.")

pc.heading("1. License & Usage", level=3)
pc.text("pyclay is licensed under the **Apache 2.0 License**. You are free to download, modify, and distribute the software for both personal and commercial projects, provided that the original copyright and permission notice is included in all copies.")

pc.heading("2. No Warranty", level=3)
pc.text("The software is provided *as is*, without warranty of any kind, express or implied. In no event shall the authors or copyright holders be liable for any claim, damages, or other liability arising from the use of the library.")

pc.heading("3. Community Guidelines", level=3)
pc.text("When participating in our community spaces (such as GitHub issues or discussions), please behave respectfully and adhere to standard open-source code of conduct expectations.")


# =========================================================================
#  GLOBAL FOOTER
# =========================================================================
pc.footer(
    text=f"© {datetime.datetime.now().year} pyclay. Open source under Apache-2.0 License.",
    variant="columns",
    columns_data=[
        {"heading": "Product", "links": [
            {"text": "Features", "href": "#features"},
            {"text": "Components", "href": "#components"},
        ]},
        {"heading": "Resources", "links": [
            {"text": "Documentation", "href": "#docs"},
            {"text": "Tutorials", "href": "#tutorial"},
            {"text": "PyPI Package", "href": "https://pypi.org/project/pyclay/"},
        ]},
        {"heading": "Community", "links": [
            {"text": "GitHub Project", "href": "https://github.com/ayush-sharma11/pyclay"},
            {"text": "Twitter / X", "href": "https://x.com/ahhyoushh"}
        ]}
    ],
    links=[
        {"text": "Privacy Policy", "href": "#privacy"},
        {"text": "Terms of Service", "href": "#terms"}
    ]
)