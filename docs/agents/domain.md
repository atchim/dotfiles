# Domain docs

How the engineering skills should consume this repo's domain
documentation when exploring the codebase.

## Before exploring, read these

- **`CONTEXT.md`** at the repo root — the glossary and the relationships
  between its terms.
- **`docs/adr/`** — the ADRs that touch the area you're about to work in.
- **`CONVENTIONS.md`** — the writing and formatting conventions every
  change is expected to follow. The root one holds the general craft
  rules; several directories carry their own
  (`dot_config/{bspwm,fish,polybar,sxhkd,tmux,private_qutebrowser}/`).
  The nearest one to the file you're editing wins, layered over the root.

If any of these files don't exist, **proceed silently**. Don't flag their
absence; don't suggest creating them upfront. The `/domain-modeling`
skill, reached via `/grill-with-docs` and
`/improve-codebase-architecture`, creates them lazily when terms or
decisions actually get resolved.

## Layout: single-context

One `CONTEXT.md` and one `docs/adr/` at the repo root, covering the whole
repo. There is no `CONTEXT-MAP.md` and there are no per-context
`CONTEXT.md` files — this is not a monorepo.

```text
/
├── AGENTS.md           ← agent skill config, points here
├── CONTEXT.md          ← glossary + relationships
├── CONVENTIONS.md      ← craft rules; per-directory ones layer on top
├── docs/
│   ├── adr/            ← 0001…0006
│   └── agents/         ← this file, issue-tracker.md, triage-labels.md
├── dot_config/         ← chezmoi source for ~/.config
├── dot_local/bin/      ← helper scripts and reconcilers
└── .chezmoiscripts/
```

That single context is deliberate. The domain clusters — display,
desktops, session layering, audio, capture — each span several
directories, because chezmoi splits config from logic: `Reconciler` is
defined by `dot_local/bin/{bspwm-monitor,polybar-launch}` but is about
polybar and bspwm, and `Layer` governs every other cluster from
`dot_config/sx/`. No directory could own a context, so don't propose
splitting `CONTEXT.md` along directory lines. Divergent vocabulary —
a second machine profile where `Tray host` means something else — would
be a real reason to revisit this; tool directories are not.

This is a chezmoi source tree, not an application source tree. Paths are
chezmoi-encoded: `dot_config/` becomes `~/.config/`, `private_` and
`executable_` are attribute prefixes, and `.chezmoiignore` keeps the
repo-only docs (`AGENTS.md`, `CONTEXT.md`, `README.md`, `docs`,
`**/CONVENTIONS.md`) out of `$HOME`. Any new repo-level doc has to be
added to `.chezmoiignore` too, or it lands in the home directory on the
next `chezmoi apply`.

## Use the glossary's vocabulary

When your output names a domain concept — in an issue title, a refactor
proposal, a hypothesis, a test name — use the term as defined in
`CONTEXT.md`, and respect its _Avoid_ list.

If the concept you need isn't in the glossary yet, that's a signal:
either you're inventing language the project doesn't use, and should
reconsider, or there's a real gap, and it's worth noting for
`/domain-modeling`.

## Flag ADR conflicts

If your output contradicts an existing ADR, surface it explicitly rather
than silently overriding:

> _Contradicts ADR-0001 (tray host is the laptop) — but worth reopening
> because…_

New ADRs go in `docs/adr/` as `NNNN-kebab-title.md`, taking the next
number; `0006` is the highest so far.
