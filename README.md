# Dotfiles

Personal dotfiles managed with [chezmoi](https://chezmoi.io).

## Managed configs

- **Bash** — `~/.bash_profile`, `~/.bashrc`
- **Alacritty** — `~/.config/alacritty/alacritty.toml`
- **bspwm** — `~/.config/bspwm/` (modular `conf.d/`; dual-monitor aware)
- **Fish** — `~/.config/fish/`
- **qutebrowser** — `~/.config/qutebrowser/`
- **Starship** — `~/.config/starship.toml`
- **sxhkd** — `~/.config/sxhkd/` (general + bspwm-specific bindings)
- **tmux** — `~/.config/tmux/tmux.conf`
- **XDG user dirs** — `~/.config/user-dirs.dirs`

Helper scripts at `~/.local/bin/`:

- `bspwm-monitor` — reconciles bspwm + xrandr to the live monitor topology.
- `bspwm-monitor-event` — srandrd callback; runs `bspwm-monitor reconcile`.

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
- [srandrd](https://github.com/jceb/srandrd) — provided via the personal
  `eslop` Gentoo overlay (`emerge x11-misc/srandrd`). Watches X RANDR events
  and runs `bspwm-monitor-event` on every monitor hotplug.

Border + presel-feedback colors are sourced live from the
[Oil 8](https://github.com/atchim/oil8) theme, which chezmoi pulls into
`~/.local/share/oil8` (see `.chezmoiexternal.toml`).

## Installation

```sh
chezmoi init --apply atchim
```

Enable pre-commit hooks after cloning:

```sh
pre-commit install
```
