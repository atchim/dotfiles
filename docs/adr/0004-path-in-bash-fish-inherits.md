# Tool PATH is defined once in `.bash_profile`; fish inherits it

Bash is the login shell (`/etc/passwd`), so `~/.bash_profile` is the single
place that builds `PATH` and exports tool-location vars (`PNPM_HOME`,
`BUN_INSTALL`, `MANPATH`) at session start. The daily interactive shell is
fish — alacritty spawns `/bin/fish` directly — yet fish carries no `PATH`
setup of its own.

This works because fish never starts from a clean environment: the login
bash sources `~/.bash_profile`, the user launches `sx` from that session, X
inherits the populated environment, and alacritty (and the fish it spawns)
inherit it in turn. Defining `PATH` a second time in fish would only let the
two copies drift — which is exactly what happened when the pnpm and bun
installers appended their own blocks to `config.fish`.

New tool paths therefore go in `dot_bash_profile` — via the `push_dir`
helper, or by sourcing a tool-provided `env` script (`~/.cargo/env`) where
one exists — never in fish config. The alternatives were rejected:
duplicating entries in both shells reintroduces drift, and a shared POSIX env
file can't be sourced by fish (incompatible syntax).

Caveat: edits to `bash_profile` reach fish only after the next full login
(TTY → `sx`), not in already-running X sessions. Installer-written PATH
blocks in fish `config.fish` are reverted on `chezmoi apply`, with their
setup relocated here.
