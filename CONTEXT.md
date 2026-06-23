# Chezmoi Dotfiles Context

Personal Linux desktop dotfiles, biased toward a bspwm + sxhkd + polybar
stack on a dual-monitor laptop (eDP plus one external). Documents the
shared vocabulary used by the helper scripts and configs in this repo.

## Language

**Bar instance**:
A running polybar process bound to a single xrandr output.
_Avoid_: panel, statusbar, bar (when ambiguous)

**Tray host**:
The one bar instance that owns the system tray. In this repo, always the
laptop.
_Avoid_: primary bar, main bar

**Reconciler**:
A script that brings live system state into agreement with desired state,
idempotently. `bspwm-monitor` and `polybar-launch` are reconcilers.
_Avoid_: sync script, fix-up, applier

**Topology**:
The current set of connected xrandr outputs and their geometric layout.
_Avoid_: layout (collides with bspwm's tiling layout), screen config

**Hardware probe**:
A runtime check against `/sys` or `xrandr` to decide whether a feature is
present (battery, backlight, wifi, external monitor).
_Avoid_: feature detection, capability check

**Hotplug event**:
An X RANDR event delivered by `srandrd` when the topology changes.
Triggers a reconcile pass.
_Avoid_: monitor change, display event

**Laptop output**:
The internal display, hard-coded as `eDP` in `bspwm-monitor`.
_Avoid_: builtin display, primary (it isn't — see ADR-0001)

**External output**:
The first non-`eDP` connected output. By convention it is xrandr-primary
when present, but is _not_ the tray host (see ADR-0001).
_Avoid_: secondary, monitor 2

**Slot**:
One of the ten desktop positions (1–10) each monitor owns. The Nth slot
on one monitor corresponds to the Nth slot on another; `bspwm-monitor`
merges windows by slot when an output detaches.
_Avoid_: workspace, tag, desktop number

**Parallel desktop**:
For a given desktop, the desktop at the same Slot on the other monitor —
e.g. the laptop's slot-3 desktop and the external's slot-3 desktop are
parallels. Sending a window to its parallel desktop relocates it across
monitors while preserving its slot, distinct from a plain cross-monitor
move (which lands on the target monitor's focused desktop).
_Avoid_: mirror (implies duplication), sibling (collides with bspwm
sibling nodes), twin

**Layer**:
The owner of an autostart. Two values: **session layer** (owned by
`sx`) and **WM layer** (owned by `bspwmrc`). The boundary is identity,
not runtime ordering: a session-layer autostart is one whose identity
is WM-agnostic (sxhkd, srandrd, dunst), even if it happens to be
configured for bspwm.
_Avoid_: piece, component, tier

**WM**:
The window manager mounted inside a session — bspwm today, potentially
others later. `sx <wm>` picks which one. Distinct from "session": a
session is the whole X bring-up (session-layer autostarts + a WM); a
WM is just the WM. Reserved CLI vocabulary: `<wm>`, not `<sesh>`.
_Avoid_: session (means the whole layer), sesh

**Autostart**:
A program launched as part of bringing the session up. May be a daemon
(sxhkd, dunst), a one-shot (fehbg, `bspwm-monitor reconcile`), or a
watcher (srandrd). Each autostart lives in exactly one Layer.
_Avoid_: service, process, startup task

**EWMH state**:
The X11 properties that surface bspwm's structure to other clients —
`_NET_DESKTOP_NAMES`, `_NET_WM_DESKTOP`, `_NET_CLIENT_LIST`. bspwm
updates these on most operations, but `_NET_WM_DESKTOP` drifts when a
node is moved across monitors and then the source monitor is removed.
`bspwm-monitor`'s `sync_ewmh_desktop` patches the drift after each
reconcile so EWMH consumers (rofi -modi window, wmctrl) see correct
desktop names instead of `n/a`.
_Avoid_: window state (collides with bspwm's per-node tiling state)

**Alsamixer scale**:
The perceptual (logarithmic-in-dB) volume percentage alsamixer displays —
the canonical "volume" number in this repo. Distinct from the raw mixer
register (`0..87` on this codec) and from amixer's dB-linear `%`. Helper
scripts (`audio-jack-monitor`) and the polybar volume ramp target it.
_Avoid_: volume %, raw volume, amixer %

**Capture mode**:
How much of the desktop the `screenshot` helper grabs. **focused** is the
focused monitor's rectangle; **root** is every connected output (the whole
X root window); **region** is a drag-selected rectangle.
_Avoid_: screen (X11 "screen" is the root — the inverse of "focused")

## Relationships

- A **Topology** has one **Laptop output** and zero or one **External
  output**.
- A **Hotplug event** triggers a **Reconciler** pass which may spawn or
  retire **Bar instances**.
- Each connected output gets one **Bar instance**; exactly one of them is
  the **Tray host**.
- **Hardware probes** run inside reconcilers, never inside config files.
- Every **Autostart** belongs to exactly one **Layer**: the session
  layer (mounted by `sx`) or the WM layer (mounted by `bspwmrc`).
- Reconcilers must keep **EWMH state** in agreement with bspwm's
  internal state when they move nodes across monitors.
- A window can be sent to its **Parallel desktop** to cross monitors
  without changing its **Slot**.
- A **Slot** can be focused across monitors: the focused monitor's
  instance wins, falling back to the other monitor's only when it alone
  holds a window.
- A **root** capture spans the whole **Topology**; a **focused** capture
  covers one monitor of it.

## Example dialogue

> **Dev:** "If I dock the laptop, does the **Tray host** move to the
> **External output**?"
>
> **Author:** "No — the **Tray host** is always the **Laptop output**,
> even though the **External output** becomes xrandr-primary on attach.
> Decoupling those is deliberate (see ADR-0001)."
>
> **Dev:** "Where does the battery name come from in the polybar config?"
>
> **Author:** "A **Hardware probe** in `polybar-launch` sets `$BAT`
> before launching. The config interpolates `${env:BAT}`. No `.tmpl`."
