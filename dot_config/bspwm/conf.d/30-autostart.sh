# shellcheck shell=sh

# Reconcile the live monitor topology against the WM. Must run last in
# bspwmrc because it re-sources 20-rules.sh after attaching an external.
# Session-layer autostarts (sxhkd, srandrd, polybar-launch) live in `sx`.
bspwm-monitor reconcile
