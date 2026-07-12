# Audio runs on PipeWire, not raw ALSA

This box deliberately ran **raw ALSA with no sound server**, to avoid the
failure its owner had hit before: one application opening the card
exclusively and locking every other client out. ALSA's `default` PCM
already software-mixes through `dmix`, so day-to-day playback was fine.

The official Spotify client broke that peace. It speaks **only**
PulseAudio, so on a serverless box its Gentoo wrapper preloads **apulse**
(a PulseAudio→ALSA shim) via `LD_LIBRARY_PATH`. apulse (0.1.14,
unmaintained) cannot survive the stream teardown/re-create Spotify does on
every next/previous track: the driver never restarts, and playback dies
with `AudioRendererImpl ... cannot start driver` / `AdvanceStuck:
audio_session_play`.

The fix is to stop avoiding a sound server and adopt the one already
installed. **PipeWire** (`media-video/pipewire`, `+pulseaudio
+sound-server +pipewire-alsa`) + **WirePlumber** own the hardware and mix
every client — ALSA, PulseAudio, all of it. `sx` autostarts it in the
**session layer** via `gentoo-pipewire-launcher` (ADR-0003; it is
WM-agnostic session plumbing, like sxhkd). The feared exclusive-device
lock is _cured_, not caused, by a server — no app touches the card
directly anymore. (PipeWire is also not the 2010s PulseAudio whose
device-stealing earned the caution; it is the modern replacement.)

## Consequences

**apulse stays installed; Spotify gets a shim, not a rebuilt wrapper.**
firefox links `apulse[sdk]` at build time whenever it is built
`+pulseaudio` (and apulse is a `world` member), so apulse cannot be
removed. Spotify's wrapper hardcodes the `/usr/lib64/apulse` preload in
the ebuild's `spotify-wrapper` template — `envsubst` substitutes only
`$SPOTIFY_HOME`/`$LIBDIR`, and no USE flag rewrites the line — so flipping
Spotify to `+pulseaudio` does **not** help while apulse exists on disk.
The lever is to skip the preload: `~/.local/bin/spotify` (ahead of
`/usr/bin` in `PATH`) launches the binary with `LD_LIBRARY_PATH` cleared,
so it resolves the real `media-libs/libpulse` → `pipewire-pulse`.
Spotify's own `pulseaudio` USE is now moot.

**`+pipewire-alsa` unifies the mixer.** Without it, PulseAudio clients
route through PipeWire but raw-ALSA clients still open the card directly —
reintroducing the exact contention this whole change removes. With it,
ALSA's `default` PCM is a PipeWire node too, so there is one mixer and
nothing to fight over.

**The volume model moved off the hardware Master.** polybar's volume
module is `internal/pulseaudio` — it follows the _default sink_ across the
box's several outputs, where `internal/alsa` was pinned to one card. The
`super + space ; m` mixer binding opens **ncpamixer**; volume mute and the
click-notify read the default sink through `wpctl`. `audio-jack-monitor`,
which forced the hardware `Master` to preset levels on jack plug, is
**retired**: WirePlumber remembers volume + mute per output port and
auto-switches on plug, doing that job natively. See the **Volume** and
**Sound server** entries in repo-root `CONTEXT.md`.

**Costs accepted.** Two always-running user daemons (`pipewire`,
`wireplumber`) where there were none — the minimalism the raw-ALSA setup
prized. Traded for: robust track-change playback, per-app volume, hotplug
and Bluetooth audio, and a single mixer that ends the device-locking risk
for good.
