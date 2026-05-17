# Session-layer autostarts live in `sx`, not `bspwmrc`

`bspwmrc` traditionally autostarts everything the user wants alongside
bspwm: sxhkd, polybar, dunst, wallpaper, the X RANDR watcher. This
conflates two layers — the WM (bspwm) and the surrounding X session —
into one script.

This repo splits them. `sx` (the session manager) mounts the **session
layer**: every autostart whose identity is WM-agnostic (sxhkd, srandrd,
`polybar-launch`, `~/.fehbg`, future dunst). `bspwmrc` owns the **WM
layer**: only programs that are part of the bspwm stack by name and
purpose (`bspwm-monitor reconcile` today).

The rule is **identity, not runtime ordering**. sxhkd's bindings call
`bspc`, so it "needs bspwm running" in the operational sense — but its
identity is a generic X hotkey daemon, not bspwm machinery, so it lives
in the session layer. By the same rule, `bspwm-monitor reconcile`
stays in `bspwmrc` because the script is bspwm-specific by name and
purpose.

Alternative considered: "anything that depends on bspwm at runtime
lives in `bspwmrc`." Rejected because it would pull sxhkd back into
`bspwmrc`, which defeats the point of having `sx` as a mounting layer.

Costs accepted: one extra config directory (`dot_config/sx/`), one
extra script (`sxrc`), and a small learning hurdle for readers used
to bspwmrc-as-everything. Trade earns: a clean swap path to a
different WM (`sx sway` becomes a new function next to `bspwm()`,
with session-layer autostarts unchanged) and a cleaner story for
adding session-wide tools (dunst, picom, clipmenu) — they don't
need to know about bspwm.

See repo-root `CONTEXT.md` for the **Layer**, **Autostart**, and
**WM** glossary entries.
