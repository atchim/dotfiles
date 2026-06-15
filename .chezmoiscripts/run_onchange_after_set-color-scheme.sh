#!/bin/sh

# Set the freedesktop color-scheme preference to dark. xdg-desktop-portal's
# gtk backend reads this gsettings key and serves it over the
# org.freedesktop.appearance namespace, so portal-aware apps — qutebrowser
# (QtWebEngine) and GTK4/libadwaita — follow it through their "auto" color
# mode. Re-runs whenever the desired value below changes.
#
# color-scheme: prefer-dark

set -eu

if ! command -v gsettings >/dev/null 2>&1; then
  printf 'set-color-scheme: gsettings not installed; skipping.\n' >&2
  exit 0
fi

gsettings set org.gnome.desktop.interface color-scheme 'prefer-dark'
