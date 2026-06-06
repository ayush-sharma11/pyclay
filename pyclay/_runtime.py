_pages = {"index": []}
_current_page = "index"
_page_config = {}
_container_stack = []
_tabs_stack = []


def reset():
    _pages.clear()
    _pages["index"] = []
    global _current_page
    _current_page = "index"
    _page_config.clear()
    _container_stack.clear()
    _tabs_stack.clear()


def set_page_config(**kwargs):
    _page_config.update(kwargs)


def get_page_config():
    return dict(_page_config)


def set_current_page(name):
    global _current_page
    _current_page = name
    if name not in _pages:
        _pages[name] = []
    # Clear the container stack when switching pages to prevent leaking containers
    _container_stack.clear()
    _tabs_stack.clear()


def get_current_page():
    return _current_page


def add(component):
    """Add a component to the current container (or top-level tree of current page)."""
    if _container_stack:
        _container_stack[-1].append(component)
    else:
        if _current_page not in _pages:
            _pages[_current_page] = []
        _pages[_current_page].append(component)


def push_container(component):
    """Push a new container onto the stack; future add() calls go into it."""
    add(component)
    _container_stack.append(component["children"])


def pop_container():
    """Pop the current container off the stack."""
    if _container_stack:
        _container_stack.pop()


def get_pages():
    return dict(_pages)


def get_tree():
    """Compatibility wrapper returning current page tree."""
    if _current_page not in _pages:
        _pages[_current_page] = []
    return list(_pages[_current_page])
