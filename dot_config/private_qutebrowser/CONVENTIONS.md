# Qutebrowser Config Conventions

App-specific architectural conventions for `dot_config/private_qutebrowser/`.
General Python idioms and universal rules live in the repo-root
`CONVENTIONS.md`.

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
`_types.py` and are imported by every domain module:

```python
from _types import ConfigAPI, ConfigContainer
```

`_types.py` exposes its surface via `__all__`. Domain modules never import
qutebrowser's internal modules directly — they only see the aliases.
