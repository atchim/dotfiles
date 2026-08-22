# Backlight writes are clamped in a helper, outside polybar's internal scroll

polybar's `internal/backlight` writes a percentage of `max_brightness` on
scroll. That is the obvious thing, it is what `enable-scroll = true` is
for, and on this panel under kernel 7.1 it turns the display off.

7.1's amdgpu sets `props.max_brightness = max` where it previously set
`max - min`, commented "min is zero, so max needs to be adjusted". This
panel's `min` is not zero (`min_input_signal = 12`, so `min = 0x101 × 12
= 3084`), so the advertised range grew **62451 → 65535** across the
kernel bump and its top values now wrap the 16-bit PWM register: 64532
gives `0xffff` (100% duty), 64533 gives `0x00e8` (0.35%), 65535 gives
1.8%. Scrolling to 100% blanks the panel, and recovering from that needs
a root write to a file the user can no longer see to find.

polybar 3.7.2 has no ceiling option, so the write leaves the module:
`enable-scroll = false`, and `%{A4}`/`%{A5}` action tags in `format` call
`polybar-backlight`, which clamps to the **Brightness ceiling**. The
module keeps `type = internal/backlight` for the read and the ramp — only
the write moved.

The action tags are not stylistic. The module-level `scroll-up` /
`scroll-down` keys are the documented way to do this and they do not work
here: on `internal/backlight` all five mouse buttons bound that way are
silently ignored, while the same commands in `%{A}` tags fire every time
(measured — see `dot_config/polybar/CONVENTIONS.md`).

## Considered Options

- **`brightnessctl`.** Resolves the backlight device itself, which would
  drop one dependency on the device name. But it knows nothing about the
  cliff, so the clamp would still be ours to write — a new dependency
  bought for nothing. Not installed.
- **Leave scroll internal and accept the cliff.** One scroll to the top
  blanks the display. Rejected.
- **`amdgpu.dcdebugmask=0x40000`** (`DC_DISABLE_CUSTOM_BRIGHTNESS_CURVE`)
  on the kernel cmdline linearises the whole range, which makes it safe
  without any userspace clamp. It discards the panel's calibrated
  brightness curve for every consumer, and it is a GRUB change belonging
  to kslop rather than to dotfiles. Deliberately not taken.

## Consequences

**The ceiling is a hardcoded constant — a deliberate exception to
ADR-0002.** Every other hardware fact in this repo is probed at launch,
but this one cannot be: the kernel advertising the wrong number _is_ the
bug, so there is nothing in `/sys` to read. It was measured. The script
uses `min(64532, max_brightness)`, so it degrades into a plain maximum
once the kernel is fixed upstream or the script meets a different panel,
rather than writing a value the kernel would reject with `-EINVAL`.

**The Brightness ceiling is the repo's 100%.** `polybar-notify` divides
by `polybar-backlight ceiling`, not by `max_brightness`, so the readout
and the scroll cannot disagree about what full brightness means. Raw
sysfs values are not user-facing.

**Non-root writes still depend on untracked system state.** The
`brightness` attribute is `root:root 0644` until
`/etc/udev/rules.d/70-backlight-video.rules` chgrp/chmods it for the
`video` group. That rule matches `KERNEL=="amdgpu_bl*"` rather than a
literal name, because amdgpu names the device after the DRM card index —
so it is `amdgpu_bl1` when the dGPU loads and `amdgpu_bl0` in the
iGPU-only profile (kslop's ADR-0007, a different document than this one).
The recovery recipe lives in kslop
`hardware/avell-storm-450-r7-8745hs/system-config.md`. When it goes
stale the failure is silent — the ramp still reads, only the write is
denied — so `polybar-backlight` says so on stderr _and_ via
`notify-send`, since `polybar-launch` discards polybar's stderr.
