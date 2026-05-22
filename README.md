# Dotfiles

Personal dotfiles managed with [chezmoi](https://chezmoi.io).

## Managed configs

- **Bash** — `~/.bash_profile`, `~/.bashrc`
- **Alacritty** — `~/.config/alacritty/alacritty.toml`
- **bspwm** — `~/.config/bspwm/` (modular `conf.d/`; dual-monitor aware)
- **dunst** — `~/.config/dunst/` (oil8 theme via `dunstrc.d/` drop-in)
- **Fish** — `~/.config/fish/`
- **Polybar** — `~/.config/polybar/` (`bars/skeleton.ini` chassis,
  per-bar configs under `bars/`, hardware-conditional modules)
- **qutebrowser** — `~/.config/qutebrowser/`
- **Starship** — `~/.config/starship.toml`
- **sxhkd** — `~/.config/sxhkd/` (general + bspwm-specific bindings)
- **tmux** — `~/.config/tmux/tmux.conf`
- **XDG user dirs** — `~/.config/user-dirs.dirs`

Helper scripts at `~/.local/bin/`:

- `bspwm-monitor` — reconciles bspwm + xrandr to the live monitor topology.
- `topology-event` — srandrd callback; runs `bspwm-monitor reconcile`
  and `polybar-launch -t eDP bspwm` on every X RANDR change.
- `polybar-launch` — `polybar-launch [-p top|bottom] [-t primary|<out>|none]
<bar>`. Spawns one polybar instance of `bars/<bar>.ini` per connected
  monitor.
- `polybar-cpu` — `custom/script` helper that emits a CPU-load-coloured
  microchip glyph for the polybar cpu module.
- `polybar-notify` — backs every status module's `click-left`; pops a
  `notify-send` bubble with the precise reading.

## Prerequisites

### Required

- [chezmoi](https://chezmoi.io)
- [pre-commit](https://pre-commit.com)
- [ShellCheck](https://github.com/koalaman/shellcheck)
- [Shellharden](https://github.com/anordal/shellharden)
- [shfmt](https://github.com/mvdan/sh)

### Optional

- [Alacritty](https://alacritty.org) with
  [Hack Nerd Font](https://www.nerdfonts.com)
- [ccache](https://ccache.dev)
- [fish](https://fishshell.com)
- [Neovim](https://neovim.io)
- [qutebrowser](https://qutebrowser.org)
- [Starship](https://starship.rs)
- [tmux](https://github.com/tmux/tmux) with
  [xclip](https://github.com/astrand/xclip)

### bspwm + sxhkd

The bspwm config drives a dual-monitor (`eDP` + one external) layout via
`~/.local/bin/bspwm-monitor` and an X RANDR watcher. Required tools:

- [bspwm](https://github.com/baskerville/bspwm),
  [sxhkd](https://github.com/baskerville/sxhkd),
  [rofi](https://github.com/davatorium/rofi) — `x11-wm/bspwm`,
  `x11-misc/sxhkd`, `x11-misc/rofi`.
- [xrandr](https://gitlab.freedesktop.org/xorg/app/xrandr) — `x11-apps/xrandr`.
  Required for the monitor reconcile script.
- [srandrd](https://github.com/jceb/srandrd) — watches X RANDR events and runs
  `topology-event` on every monitor hotplug. Wired into srandrd by `sx`.

Border + presel-feedback colors are sourced live from the
[Oil 8](https://github.com/atchim/oil8) theme, which chezmoi pulls into
`~/.local/share/oil8` (see `.chezmoiexternal.toml`).

### Polybar

- [polybar](https://polybar.github.io) — `x11-misc/polybar` built with
  USE flags `+ipc +alsa +network` (polybar-msg, internal/alsa for the
  volume module, internal/network for the wifi module). `+pulseaudio`
  is intentionally off — this system is ALSA-focused.
- [Hack Nerd Font Mono](https://www.nerdfonts.com) — secondary font in
  the bar's stack. siji (`Wuncon Siji` upstream) is primary; auto-pulled
  by `.chezmoiexternal.toml` to `~/.local/share/fonts/siji.pcf`, with
  `dot_config/fontconfig/conf.d/30-allow-siji.conf` whitelisting it
  against Gentoo's default bitmap-font blacklist.
- Hardware is probed at launch (`/sys/class/power_supply`,
  `/sys/class/backlight`, `/sys/class/net`); modules whose hardware is
  absent are omitted from `modules-right`. See
  `docs/adr/0002-runtime-hardware-detection.md`.

Polybar is launched by `sx` (the session-layer mounter) at session start
and relaunched on every X RANDR change via the `topology-event` callback.
`super + b` toggles visibility; `super + ctrl + l ; b` restarts in place.
See `docs/adr/0003-session-layer-autostarts-in-sx.md` for the split.

Click-actions on the bar use `notify-send` to surface the precise reading
of each status module (see `dot_config/polybar/CONVENTIONS.md` — _Wordless
Status_). They need:

- [libnotify](https://gitlab.gnome.org/GNOME/libnotify) —
  `x11-libs/libnotify`. Provides `notify-send`.
- [dunst](https://dunst-project.org) — `x11-misc/dunst`. Notification
  daemon that renders the bubbles; autostarted by `sx`, themed via the
  `dunstrc.d/oil8.conf` drop-in symlinked to `~/.local/share/oil8/dunst/`.
- [wireless-tools](https://hewlettpackard.github.io/wireless-tools/) —
  `net-wireless/wireless-tools`. Provides `iwgetid` for the wifi
  click-action.
- [alsa-utils](https://alsa-project.org/wiki/Main_Page) —
  `media-sound/alsa-utils`. Provides `amixer` for the volume click-action
  and `alsamixer` (bound to `super + space ; m`).

## Installation

```sh
chezmoi init --apply atchim
```

Enable pre-commit hooks after cloning:

```sh
pre-commit install
```

## Conventions

Style and structure rules used in this repo live in `CONVENTIONS.md`
(universal) and per-app `CONVENTIONS.md` files alongside each config.
