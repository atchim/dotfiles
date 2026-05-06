# tmux Conventions

Conventions for `dot_config/tmux/`. Universal rules live in repo-root
`CONVENTIONS.md`.

## Modular `conf.d/`

`tmux.conf` is a thin entry point. All real configuration lives in
`conf.d/*.conf`, sourced in lexical order:

```text
conf.d/
├── 00-options.conf      # server/session options
├── 01-terminal.conf     # terminal capability tweaks
├── 02-navigation.conf   # prefix + pane/window movement
├── 03-splits.conf       # split + resize bindings
├── 04-copy-mode.conf    # vi-style copy mode
├── 05-status.conf       # status-line config
└── 06-ui.conf           # visual styling
```

Number prefixes establish load order; each file owns one topic. Add new
files at the slot that reflects _when_ they need to load, not their
alphabetical name.

## Modeline

Each `conf.d/*.conf` ends with `# vim: ft=tmux` so vim picks up the
filetype on the ambiguous `.conf` extension. (See root `CONVENTIONS.md`
for the general modeline rule.)
