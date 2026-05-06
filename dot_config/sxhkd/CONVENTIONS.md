# sxhkd Conventions

Conventions for `dot_config/sxhkd/`. Universal rules live in repo-root
`CONVENTIONS.md`.

## Per-Binding Comment

Every binding gets a one-line `#` comment immediately above it (no blank
line between). The comment describes what the binding does, not what keys
are pressed — the keys are already self-documenting.

```sxhkd
# Reload sxhkd config without restarting.
super + Escape
  pkill -USR1 -x sxhkd

# Cycle to the next desktop on the focused monitor.
super + Tab
  bspc desktop -f next.local
```

## Modifier Order

Canonical order, left to right: `super → ctrl → alt → shift → key`. Every
binding follows it.

```sxhkd
# Good.
super + ctrl + shift + r

# Bad.
shift + super + ctrl + r
```

## Section Layout

Universal `Labels` rules apply (Setext H2 for segments). The per-binding
comment requirement is additional — it doesn't replace section labels; it
co-exists with them.

```sxhkd
# Window Management
# -----------------

# Close the focused window.
super + w
  bspc node -c

# Toggle floating state.
super + shift + space
  bspc node -t '~floating'
```
