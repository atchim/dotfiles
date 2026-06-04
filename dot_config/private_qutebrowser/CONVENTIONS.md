# qutebrowser Conventions

Conventions for `dot_config/private_qutebrowser/`. Universal rules live
in repo-root `CONVENTIONS.md`.

## Python

- Tuple `(...)` for fixed sequences; list `[...]` only when the contents
  will mutate.
- Type hints on every function signature.
- Leading underscore for module-private names (`_DOMAINS`, `_helper`).
- `__all__` for modules that exist purely to re-export names.

## Domain-Module Pattern

Each domain (tabs, content, search, …) lives in its own module and exposes
a single `setup` function:

```python
def setup(c: ConfigContainer, config: ConfigAPI) -> None:
    c.tabs.position = 'top'
    c.tabs.show = 'always'
    config.bind('<space>tp', 'config-cycle tabs.position top left')
```

`config.py` owns the orchestration: it lists every domain in `_DOMAINS`,
imports or reloads each, and calls its `setup`. Adding a new domain is
two steps — drop a `{name}.py` exposing `setup`, append `'name'` to
`_DOMAINS`. No other file changes.

## Shared Type Aliases

Type aliases for the qutebrowser-injected `c` and `config` globals live in
`_qute_types.py` and are imported by every domain module:

```python
from _qute_types import ConfigAPI, ConfigContainer
```

`_qute_types.py` exposes its surface via `__all__`. Domain modules never import
qutebrowser's internal modules directly — they only see the aliases.

The name avoids `_types`: Python 3.14 ships a built-in `_types` module, and
built-in finders run before the path finder, so a local `_types.py` would be
shadowed (`cannot import name 'ConfigAPI' from '_types'`).
