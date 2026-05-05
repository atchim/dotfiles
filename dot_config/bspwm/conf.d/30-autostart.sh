# shellcheck shell=sh

# Bring monitors + desktops into a known state, then start the helpers
# that keep them there (RandR watcher) and the keybinding daemon.

# Initial reconcile uses live xrandr/bspwm state, so it works whether bspwm
# is starting laptop-only, with the external pre-attached, or after a restart.
bspwm-monitor reconcile

# Watch X RANDR for monitor hotplug; every event re-runs reconcile.
if ! pgrep -x srandrd >/dev/null 2>&1; then
  srandrd -n bspwm-monitor-event &
fi

# sxhkd: load both the general bindings and the bspwm-specific ones.
if ! pgrep -x sxhkd >/dev/null 2>&1; then
  _sxhkd_dir="${XDG_CONFIG_HOME:-$HOME/.config}/sxhkd"
  sxhkd -c "${_sxhkd_dir}/sxhkdrc" -c "${_sxhkd_dir}/bspwm.sxhkdrc" &
  unset _sxhkd_dir
fi
