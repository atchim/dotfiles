# Polybar adapts to hardware at runtime, not at chezmoi-apply time

In a chezmoi-managed repo, the obvious way to handle hardware variance
(which battery is present, which backlight card, which wifi interface,
how many monitors) is `.tmpl` files resolved at `chezmoi apply` time.

We instead detect hardware **at polybar launch** via probes in
`polybar-launch`, which exports environment variables (`BAT`,
`BACKLIGHT`, `WIFI`, `MONITOR`, `TRAY`, `MODULES_RIGHT`) that the
`.ini` configs interpolate with `${env:VAR}`. The configs themselves
are static and machine-agnostic.

Rationale: hardware changes between `chezmoi apply` runs. Docking
adds a monitor, battery replacement renames `BAT0` to `BAT1`, a
USB wifi dongle adds an interface. Hotplug-friendliness matters more
than chezmoi-nativeness, and the existing `bspwm-monitor` reconciler
already pioneered this same runtime-probe pattern for the bspwm side.
`polybar-launch` is its polybar-side counterpart and is invoked from
the topology hotplug callback (`topology-event`), alongside
`bspwm-monitor reconcile`. The callback lives in `dot_local/bin/`
and is wired into srandrd by `sx`.
