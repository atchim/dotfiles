# bspwm Conventions

App-specific conventions for `dot_config/bspwm/` and its helper scripts in
`dot_local/bin/`. Universal rules and POSIX shell conventions live in the
repo-root `CONVENTIONS.md`.

## Modular `conf.d/`

`bspwmrc` is a thin entry point. All real configuration lives in
`conf.d/*.sh`, sourced in lexical order:

```text
conf.d/
├── 00-options.sh    # bspc config knobs (border, gaps, splits)
├── 10-colors.sh     # border/presel colors
├── 20-rules.sh      # bspc rule -a entries
└── 30-autostart.sh  # one-shot programs (sxhkd, picom, …)
```

Number prefixes carve out load-order tiers (`00-` options, `10-` colors,
`20-` rules, `30-` autostart). Add new files into the tier that reflects
_when_ they need to run, not their alphabetical name.

Each `conf.d/*.sh` opens with `# shellcheck shell=sh` — they're sourced
under POSIX, not bash.

## Helper-Script Pair

Monitor reconciliation is split across two scripts in `dot_local/bin/`:

- `bspwm-monitor` — the worker. Holds the topology rules and the
  reconcile logic. Idempotent; can be invoked from anywhere.
- `bspwm-monitor-event` — the srandrd callback. Receives the X RANDR
  event, ignores it (reconciliation reads live state), and calls
  `bspwm-monitor reconcile`.

The split is deliberate: the worker is callable manually (debugging, one-off
fix-ups), the callback is wired into the X RANDR event loop. Keeping the
event handler trivial means topology logic only needs to be tested in one
place.

`bspwm-monitor` exposes subcommands as aliases of `reconcile`
(`init`, `attach`, `detach`) so the autostart hook and the hotplug callback
can name their intent without branching the worker's logic.
