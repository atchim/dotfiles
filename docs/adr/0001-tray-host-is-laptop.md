# Tray host is a launch-time flag; convention is to pass the laptop

Polybar requires one bar instance to own the system tray. `polybar-launch`
exposes the choice via `-t / --tray`, accepting `primary` (default — resolves
to xrandr's `--primary` output), an explicit output name (e.g. `eDP`), or
`none`.

The convention this repo follows at the **invocation layer** is `-t eDP`:
the laptop is the constant monitor and never hotplugs, so passing the
laptop output keeps tray-icon positions stable across docking events. With
`-t primary` (the default), the tray would jump between bars whenever
`bspwm-monitor` re-flagged the external as primary on attach/detach. The
laptop convention costs one short flag and earns muscle-memory stability.

This decision used to be hardcoded inside `polybar-launch`; v2 of the script
moved it to a flag so future bars (notifications, music, etc.) can opt out
or pick a different host without script edits.
