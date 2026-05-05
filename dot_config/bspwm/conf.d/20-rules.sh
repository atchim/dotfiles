# shellcheck shell=sh

# Drop any prior rules so a re-source from the rearrange script is idempotent.
bspc rule --remove '*:*'

# Browsers
# --------

# Pin to focused monitor's `browse` slot, follow focus.

bspc rule --add Chromium-bin-browser-chromium desktop='focused:^2' follow=on
bspc rule --add Chromium-browser-chromium desktop='focused:^2' follow=on
bspc rule --add firefox desktop='focused:^2' follow=on
bspc rule --add 'firefox:Toolkit:Picture-in-Picture' state=floating sticky=on
bspc rule --add Google-chrome desktop='focused:^2' follow=on
bspc rule --add qutebrowser desktop='focused:^2' follow=on
bspc rule --add Vivaldi-stable desktop='focused:^2' follow=on

# State rules
# -----------

bspc rule --add '*:popup' state=floating
bspc rule --add vlc state=floating
bspc rule --add Zathura state=tiled

# Image editors
# -------------

# Follow focus when a child window spawns.

bspc rule --add Aseprite follow=on
bspc rule --add Darktable follow=on
bspc rule --add Gimp follow=on
bspc rule --add Inkscape follow=on
bspc rule --add krita follow=on

# Dialogs/Pinentry: Floating
# --------------------------

bspc rule --add Pinentry state=floating
bspc rule --add Pinentry-gtk state=floating
bspc rule --add Polkit-gnome-authentication-agent-1 state=floating
