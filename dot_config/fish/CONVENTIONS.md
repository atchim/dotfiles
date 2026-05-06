# fish Conventions

Conventions for `dot_config/fish/`. Universal rules live in repo-root
`CONVENTIONS.md`.

## Directory Layout

- `conf.d/*.fish` — per-topic configuration. Fish sources every file in
  this directory before `config.fish`.
- `config.fish` — reserved for startup logic that must run _after_
  `conf.d/`. Empty or near-empty in normal use.
- `functions/{name}.fish` — one function per file. Fish autoloads each
  function on first call by its filename.
- Tiny `conf.d/*.fish` files don't get a header docstring — the
  filename is the documentation.

## Function Documentation

Document functions with the `--description` flag, never with a `#` comment
above the definition. Fish surfaces `--description` in `funced`, `type
{name}`, completion hints, and the web config — a comment doesn't.

```fish
function ls --wraps eza --description 'Alias for eza'
    eza $argv
end
```

When a function wraps a command (alias-style), pass `--wraps cmd` so
completions inherit from the wrapped command.

## Variable Scope

Use `set -g` as the default scope for session variables under `conf.d/`.
Universal scope (`set -U`) writes to disk and persists across sessions —
reach for it only when persistence is the explicit goal.
