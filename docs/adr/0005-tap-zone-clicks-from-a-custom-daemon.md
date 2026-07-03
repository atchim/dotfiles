# Tap-zone clicks come from a custom daemon, not native libinput

libinput's tap-to-click chooses a button by finger **count** — one, two,
or three fingers map to left, right, middle — and can never pick a button
by **where** on the pad the tap lands. We want zone-based clicks: a
single-finger tap acts as left, right, or middle depending on its
position, mirroring the `button_areas` split of a physical clickpad press
(see the **Tap-zone click** entry in repo-root `CONTEXT.md`). Native
libinput cannot express that, so the session autostarts `tapzoned`
(`~/repo/tapzoned`) — an evdev reader that watches the pad read-only and
injects the click itself — instead of enabling native `Tapping`.

Consequences. Native tapping stays off (it is already the libinput
default on this box, and this repo enables it nowhere), so the daemon and
libinput never both fire — no defensive `xinput set-prop` is needed.
`tapzoned` is a WM-agnostic input daemon, so it mounts in the **session
layer** (`sx`), not `bspwmrc` (ADR-0003). The backend is pinned to
`--backend xtest` rather than left on `auto`: this box's kernel lacks
`CONFIG_INPUT_UINPUT`, which makes `auto`'s no-display uinput fallback a
dead end, and pinning states the mount's real backend and fails honestly
if `DISPLAY` is ever absent.
