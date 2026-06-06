# Contributing to pyclay

Thanks for your interest in contributing! Here's how to get started.

## Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ayush-sharma11/pyclay.git
   cd pyclay
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/macOS
   venv\Scripts\activate      # Windows
   ```

3. **Install in development mode with dev dependencies:**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Run the example app:**
   ```bash
   pyclay run examples/app.py
   ```

## Running Tests

```bash
pytest
```

## Project Structure

```
pyclay/
├── pyclay/              # The library package
│   ├── __init__.py      # Public API (all pc.* functions)
│   ├── _cli.py          # CLI entry point (run / build)
│   ├── _renderer.py     # HTML generation engine
│   ├── _runtime.py      # Component tree state management
│   └── _server.py       # Dev server with hot reload
├── tests/               # Test suite
├── examples/            # Example apps
├── pyproject.toml       # Package metadata & build config
└── CHANGELOG.md         # Release history
```

## Making Changes

1. **Fork** the repository and create a new branch from `main`.
2. Make your changes and add tests if applicable.
3. Ensure all tests pass: `pytest`
4. **Commit** with a clear, descriptive message.
5. Open a **Pull Request** against `main`.

## Guidelines

- Keep the public API simple — every function should be intuitive for someone who's never written HTML.
- All public functions in `__init__.py` should have docstrings.
- Maintain backward compatibility where possible.
- If adding a new component, add a corresponding example in the demo app and a test.

## Reporting Bugs

Open an issue at [github.com/ayush-sharma11/pyclay/issues](https://github.com/ayush-sharma11/pyclay/issues) with:
- Python version
- OS
- Steps to reproduce
- Expected vs actual behavior

## License

By contributing, you agree that your contributions will be licensed under the [Apache 2.0 License](LICENSE).
