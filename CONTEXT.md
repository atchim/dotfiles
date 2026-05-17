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

## Relationships

- A **Topology** has one **Laptop output** and zero or one **External
  output**.
- A **Hotplug event** triggers a **Reconciler** pass which may spawn or
  retire **Bar instances**.
- Each connected output gets one **Bar instance**; exactly one of them is
  the **Tray host**.
- **Hardware probes** run inside reconcilers, never inside config files.

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
