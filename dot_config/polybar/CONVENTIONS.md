# Polybar Conventions

Conventions for `dot_config/polybar/` and its launcher in `dot_local/bin/`.
Universal rules live in repo-root `CONVENTIONS.md`. Domain terms live in
repo-root `CONTEXT.md`. Hard-to-reverse decisions live in `docs/adr/`.

## Build Requirements

The config depends on these `x11-misc/polybar` USE flags:

- `+ipc` — `polybar-msg` (toggle, restart bindings) and `enable-ipc = true`.
- `+alsa` — `internal/alsa` for the volume module on this ALSA-focused system.
- `+network` — `internal/network` for the wifi module.

Not needed: `+pulseaudio` (we use ALSA), `+curl`, `+i3wm`, `+mpd`. Runtime
dependencies (libnotify, wireless-tools, alsa-utils, dunst) are listed in
the root `README.md`.

## Layout

```text
dot_config/polybar/
├── CONVENTIONS.md
├── bars/
│   ├── skeleton.ini   # [bar/skeleton] + oil8/module includes; chassis
│   └── bspwm.ini      # [bar/bspwm] inherit = bar/skeleton; geometry + modules
└── modules/
    ├── backlight.ini
    ├── battery.ini
    ├── bspwm.ini
    ├── cpu.ini
    ├── date.ini
    ├── volume.ini
    └── wifi.ini
```

`bars/skeleton.ini` carries everything every bar shares: oil8 colour
include, all module includes, font stack, padding, cursor settings,
`enable-ipc`. It declares `[bar/skeleton]` — _not_ a launchable bar; it's
a parent for `inherit`.

Each real bar in `bars/<name>.ini` opens with
`include-file ~/.config/polybar/bars/skeleton.ini` and then declares its
own `[bar/<name>] inherit = bar/skeleton`, overriding only what varies per
bar (geometry, position, module lists, tray-position). The filename, the
section name, and the `<bar>` argument to `polybar-launch` all match.

`polybar-launch <bar>` resolves `<bar>` → `bars/<bar>.ini` and invokes
`polybar -c <file> <bar>` once per connected monitor. Per-monitor
differences (tray host, output name) are passed via environment variables,
not by introducing extra `[bar/*]` sections.

## Theming

All colours come from oil8, referenced by name (`${oil8.eerie-black}`,
`${oil8.bone}`, …). Never write hex literals in module files — they
diverge from the theme silently when oil8 updates.

The oil8 palette is included by `bars/skeleton.ini` from
`~/.local/share/oil8/polybar/oil8.ini` (pulled by `.chezmoiexternal.toml`).
Polybar expands `~` in `include-file`, so no template indirection is
needed.

## Fonts and Glyphs

Two-font stack in `[bar/skeleton]`:

```ini
font-0 = Wuncon Siji:pixelsize=10;1
font-1 = Hack Nerd Font Mono:pixelsize=10;1
```

`Wuncon Siji` (siji's upstream fontconfig family name) is listed first
so polybar's codepoint lookup prefers its bitmap glyphs in the Private
Use Area — they render crisper at the bar's small pixel size than Nerd
Font's vector forms. The workspace digit labels are deliberately drawn
from siji's own bitmap digits (see below) for this reason, not from
ASCII. `Hack Nerd Font Mono` covers Latin text and every Nerd Font
glyph not present in siji.

siji ships at `~/.local/share/fonts/siji.pcf` via
`.chezmoiexternal.toml`. Two further pieces make it discoverable on
Gentoo:

- `.chezmoiscripts/run_onchange_after_install-siji.sh.tmpl` runs
  `fc-cache -f` automatically when the install changes.
- `dot_config/fontconfig/conf.d/30-allow-siji.conf` whitelists the
  `Wuncon Siji` family for bitmap rendering, overriding Gentoo's
  default `70-no-bitmaps-except-emoji.conf` which would otherwise
  hide it.

siji's actual codepoint range is U+E001–U+E276, and its coverage is
narrower than the old dotsoup config suggested — it does **not**
contain battery or cpu glyphs. The U+E83A / U+E96x codepoints
the old config used were Nerd Font v2's legacy Material Design Iconic
block (U+E63E–U+EB68), which Nerd Font v3 dropped. Don't trust those
codepoints in a v3 environment.

Verified siji codepoints used in this config. siji carries no semantic
glyph names for most of these (the font reports bare `U+E1xx`), so they
are identified by appearance and role:

| Codepoint(s)   | Glyph              | Used for                         |
| -------------- | ------------------ | -------------------------------- |
| U+E1A1         | terminal/console   | `tty` / `tty.x` workspace icon   |
| U+E1A0         | compass            | `browse` / `browse.x` icon       |
| U+E176..U+E17C | bitmap digits 3..9 | `d3..d9` workspace labels        |
| U+E173         | bitmap digit 0     | `d0` workspace label (10th slot) |
| U+E136         | tiled windows      | `label-tiled` layout             |
| U+E130         | single square      | `label-monocle` layout           |
| U+E135         | floating windows   | `label-floating` layout          |
| U+E13A         | pseudotiled        | `label-pseudotiled` layout       |
| U+E1F6         | pin                | `label-sticky` node-state        |
| U+E1E2         | bookmark           | `label-marked` node-state        |
| U+E0A9         | eye                | `label-private` node-state       |
| U+E258..U+E25C | signal bars        | wifi `ramp-signal` (5 levels)    |
| U+E234         | sun                | backlight ramp                   |
| U+E04E         | speaker, silent    | `ramp-volume-0`                  |
| U+E204         | speaker            | `ramp-volume-1`                  |
| U+E050         | speaker, one wave  | `ramp-volume-2`                  |
| U+E203         | speaker, waves     | `ramp-volume-3`, `-4` (loud)     |
| U+E04F         | speaker, muted (×) | `label-muted`                    |

Everything else falls to Nerd Font v3 via `font-1`:

1. FontAwesome (`nf-fa-*`, U+F000–U+F2FF) — battery ramp (U+F240..U+F244),
   bolt (U+F0E7), and the two bspwm node-state glyphs siji lacks:
   fullscreen (U+F065) and locked (U+F023).
2. Material Design (`nf-md-*`, U+F0001+) — reserved fallback for when FA
   lacks a semantic; not currently used by any module.

Never emoji, never `Unifont`. The old dotsoup config used emojis for
non-siji glyphs (moon-phase backlight, globe/dice workspaces) and they
rendered as missing-glyph boxes — there was no emoji-capable bitmap
font in the stack. Nerd Font Mono is the modern replacement for that
role.

To inspect a font's actual coverage, use `xfd -fa '<family>:pixelsize=10'`
or query its charset with `fc-query -f '%{charset}\n' <file>`.

## Wordless Status

Status modules speak through two channels — never through text:

- **Glyph shape** encodes level when a graded glyph exists. The battery
  ramp has five capacity icons, the volume ramp has mute/low/high.
- **Foreground colour** encodes severity:
  - `${oil8.chinese-green}` — safe / full / good
  - default foreground (`${oil8.bone}`) — normal
  - `${oil8.macaroni-and-cheese}` — warn
  - `${oil8.english-red}` — alert / depleted / disconnected
  - `${oil8.cyber-grape}` — muted / dimmed / inactive

Both channels run independently: a battery at 15% shows the empty-glyph
_and_ a red foreground; one signals shape, the other signals urgency.

No status module renders letters or digits in the bar. If a module can't
express its reading via the polybar internal tags (e.g. `internal/cpu`
has no aggregate-load ramp), it becomes a `custom/script` module with a
small helper in `dot_local/bin/` that emits a colour-tagged glyph. The
helper writes its current value to a state file so click-actions can
read it back.

The **`date` module is the exception**: its value (the time) IS the
content, not a status reading. Showing it directly is correct.

### Detail on demand

Polybar has no native tooltip mechanism. The closest substitute is
**`click-left` fires `notify-send`** with the current reading:

```ini
click-left = polybar-notify battery
```

`polybar-notify` (in `dot_local/bin/`) is the single helper that backs
every module's click-left — one subcommand per module (`battery`,
`backlight`, `cpu`, `volume`, `wifi`). Consolidating into one script
avoids four near-identical one-liner helpers and keeps shell-escape
cascades out of polybar's ini parser.

The bar stays wordless; the precise number is one click away.

## Hardware-Conditional Modules

Modules that depend on hardware (`battery`, `backlight`, `wifi`) read
their target via env var, not by hard-coding a name:

```ini
[module/battery]
battery = ${env:BAT}
adapter = ${env:ADAPTER}
```

The presence/absence decision happens in `polybar-launch`, which probes
`/sys` and composes `MODULES_RIGHT`. The config uses
`modules-right = ${env:MODULES_RIGHT}`. Modules whose hardware is absent
are simply not listed in `MODULES_RIGHT` — they're never instantiated,
so polybar logs no errors. See `docs/adr/0002-runtime-hardware-detection.md`.

## Workspace Icons

The bspwm desktop set is `tty browse d3 d4 d5 d6 d7 d8 d9 d0` on the
laptop and `tty.x browse.x d3.x … d0.x` on the external. Workspace
icons map by **literal desktop name**, all rendered from siji bitmaps:

- `tty` / `tty.x` → terminal glyph
- `browse` / `browse.x` → compass glyph
- `d3..d9` / `d3.x..d9.x` → siji digit `3`..`9`
- `d0` / `d0.x` → siji digit `0` (the 10th slot)

`pin-workspaces = true` scopes each bar instance to its monitor's
desktops, so the laptop bar never shows `.x` slots and vice versa.

## Tray

The tray is a regular module (`[module/tray]`, `type = internal/tray`)
defined in `modules/tray.ini` — not the deprecated `tray-position`
bar-level key. Exactly one bar instance owns it per `polybar-launch`
invocation, selected by `-t / --tray` (default `primary`). The launcher
prepends `tray` to `MODULES_RIGHT` on the chosen host instance — so tray
icons sit left of the status cluster (cpu, volume, …, date), keeping the
date right-anchored; other instances get the same module list without
the tray. Convention here is to pass
`-t eDP` so the tray's physical location stays stable across docking
events. See `docs/adr/0001-tray-host-is-laptop.md`.

## Launcher

```text
polybar-launch [-p|--position top|bottom] [-t|--tray primary|<out>|none] <bar>
```

`polybar-launch` (in `dot_local/bin/`) is the single entry point. It
probes hardware, composes `MODULES_RIGHT`, resolves the tray host, kills
any running polybar processes, and spawns one instance per connected
monitor — all using `[bar/<bar>]` from `bars/<bar>.ini`.

Position and tray host are runtime flags (defaults `bottom` and `primary`)
so the same bar config can be invoked in different shapes without editing
files. Hardware presence is probed on each launch; modules whose hardware
is absent are omitted from `MODULES_RIGHT` rather than instantiating and
erroring (see `docs/adr/0002-runtime-hardware-detection.md`).

Polybar is **launched manually** — `bspwm` and `sxhkd` configs no longer
reference polybar (and vice versa); each component is its own concern. A
future `sx` session orchestrator will bring them together. For now, run
`polybar-launch -t eDP bspwm` by hand after `startx`.

Bindings in `dot_config/sxhkd/sxhkdrc`:

- `super + b` — toggle visibility via `polybar-msg cmd {hide,show}` (sxhkd
  same-LHS body-alternation cycles successive presses), explicitly
  clearing bspwm's `bottom_padding` on hide because polybar's hidden
  window keeps its strut.
- `super + ctrl + l ; b` — `polybar-msg cmd restart` (re-reads the loaded
  config; does not re-probe hardware — for that, re-run `polybar-launch`).

The launcher remains idempotent so re-invoking it on a topology change
(e.g. plugging an external monitor) gives a fresh per-monitor set of
bars.
