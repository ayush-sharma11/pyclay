# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.1] - 2026-06-06

### Changed
- Transformed mobile view navbar to a modern slide-in sidebar with backdrop blur and close events.
- Removed border from mobile hamburger button.

## [1.1.0] - 2026-06-06

### Added
- Added `theme_switcher` option in `pc.page_config` to lock site theme and disable switcher dropdown.
- Added graceful shutdown handling to dev server (clean stop without python tracebacks).

### Fixed
- Fixed theme name syncing bug in dropdown when restoring cached theme from localStorage on page refresh.

## [1.0.0] - 2026-06-06

### Added
- 4 built-in themes: Ivory, Nebula, Arctic, and Obsidian with live switching via navbar dropdown
- Hot reload dev server (`pyclay run`) with automatic browser refresh on file save
- Static HTML export (`pyclay build`) with hot-reload script auto-stripping
- Multi-page support with hash-based routing
- 20+ components: heading, text, card, table, metric, progress bar, accordion, tabs, alert, badge, button, link button, image, video, code block, blockquote, lists, and more
- Responsive column layout system that stacks on mobile (<768px)
- Syntax-highlighted code blocks via Prism.js (Python, Bash, JS, CSS)
- Navbar with hamburger menu on mobile
- Footer with simple and multi-column variants
- Custom styling support via `style` dict on every component
- `assets/` folder support for static files (images, videos, favicon)
- Auto-detection of `assets/favicon.ico`
- CLI with `run` and `build` commands
- Error overlay in dev mode with friendly traceback display
