# Conventions

## Terminology

- **Clause** — a sequence of consecutive lines addressing a single, focused
  goal.
- **Section** — a set of clauses separated by blank lines, each tackling a
  distinct aspect of a common theme.
- **Segment** — a set of blocks (where _block_ means a clause or a section)
  forming a broader logical unit.
- **Label** — a word or noun phrase, in a comment, that names the subject of a
  block.

## Code

Three principles to apply when writing or reviewing code. They overlap at the
edges, but each prompts a different question during review.

### Let Structure Communicate Intent

The shape of the code should make the goal visible without reading the
contents.

```python
# Bad.
_MINIMAL = (
  'set tabs.show never ;; '
  'set statusbar.show in-mode ;; '
  'set scrolling.bar never'
)

# Good — the structure reads as what it is: a list of commands joined by `;;`.
_MINIMAL = ';;'.join(
  [
    'set tabs.show never',
    'set statusbar.show in-mode',
    'set scrolling.bar never',
  ]
)
```

### Prefer Correctness by Construction Over Correctness by Discipline

Choose patterns where mistakes are hard to make in the first place, not
patterns that work only if every contributor is careful. The example above
also demonstrates this: the `Bad` form silently breaks if a contributor
forgets a trailing semicolon or inserts a stray comma; the `Good` form makes
both mistakes structurally impossible.

### Use the Idioms of the Language at Hand

Write the way fluent speakers of the language write. If a language offers a
construct for the operation you're doing, reach for it before rolling your
own.

```sh
# Bad — manual loop where a shell idiom exists.
result=''
for item in "$@"; do
  result="$result $item"
done

# Good — `set --` and `"$*"` are the idiomatic way to join positional args.
set -- "$@"
result="$*"
```

## Comments

- Don't explain the obvious; never duplicate what the code already says.
- Keep comments concise.
- Write every comment as valid Markdown. Multi-line comments separate
  paragraphs with bare `#` (or `//`) lines; inline code uses backticks; URLs
  use `<angle brackets>` or `[text](url)`.
- Cite sources when a snippet is non-trivial _or_ lifted from elsewhere
  (Stack Overflow, blog post, upstream docs). Trust the contributor's
  judgement on the threshold.

  ```tmux
  # Add support for underline color.
  # SEE: <https://evantravers.com/articles/2021/02/05/curly-underlines-in-kitty-tmux-neovim/>
  set -ag terminal-overrides ',*:Setulc=\E[58::2::%p1%{65536}%/%d::%p1%{256}%/%{255}%&%d::%p1%{255}%&%d%;m'
  ```

### Tags

A closed list. Use `TAG: text` — capital tag, colon, single space, then text.
The tag opens the comment; no leading prose. Multi-line continuation indents
to align with the text after the colon.

| Tag      | Meaning                                                                                     |
| -------- | ------------------------------------------------------------------------------------------- |
| `TODO:`  | Intentional future work; code is currently fine without it.                                 |
| `FIXME:` | Known bug or incorrect behavior; fix before relying on it.                                  |
| `HACK:`  | Works, but the approach is ugly or fragile; explain why and what's better.                  |
| `NOTE:`  | Non-obvious context a reader needs. Use sparingly — if a normal comment carries it, no tag. |
| `SEE:`   | Pointer to an external resource (URL, file path, ticket).                                   |

```sh
# TODO: rewrite this when bspwm gains native multi-monitor reconcile;
#       the X RANDR watcher is a workaround.
```

### Labels

Labels name the subject of a block via a comment. Two formats:

- **H2 (segment label)** — names a code segment. Setext H2 only:

  ```rust
  // Setup
  // -----

  use std::fs;
  let config = Config::load("settings.toml");
  ```

- **H1 (file title)** — optional, at most one per file. Use only when the
  filename is opaque (`bspwmrc`, `sxhkdrc`, `.bashrc`):

  ```sxhkd
  # Bspwm Bindings
  # ==============

  # Window Management
  # -----------------
  ...
  ```

**Format rules:**

- Underline length matches the title length exactly. `Setup` (5) → `-----`
  (5).
- Exactly one blank line between the underline and the first content line.
- Setext applies to **code segments only**. Markdown documents use ATX
  (`# Title`) — different medium, different convention.
- Title case for label text (capitalize all major words; lowercase short
  conjunctions and prepositions: `a`, `the`, `and`, `or`, `to`, `of`, `in`,
  `on`, `up`, …). Hyphenated compounds capitalize both halves: `Read-Only
Mode`. No formal rulebook — natural intuition is enough.

**When to label:**

A label is required whenever the reader can't recover the segment's internal
structure from blank lines and subject shift alone. Once _any_ block in a
segment carries a label, every _subsequent_ sibling must also carry one — an
unlabeled block after a labeled one gets visually absorbed into the previous
label's scope (the same way a paragraph after an `## H2` heading reads as
belonging to that heading).

```rust
// Allowed — no labels at all (uniform segment).
let a = ...;

let b = ...;

// Allowed — unlabeled preamble, then labels begin.
let a = ...;

// Validation
// ----------
config.validate();

// Forbidden — labeled block, then unlabeled sibling absorbed into its scope.
// Setup
// -----
let a = ...;

let b = ...;        // Reads as "Setup"; might mean something else.
```

**When not to label:**

Drop the label when every line of a clause is obviously about the same
subject. The label adds visual weight without adding meaning.

```python
# Bad — every line already says `c.colors.hints` or `c.hints`.
# Hints
c.colors.hints.bg = p['eerie_black']
c.colors.hints.fg = p['bone']
c.hints.border = f"1px solid {p['chinese_green']}"
```

**Boxed/extended-ruler labels are forbidden:**

```javascript
// Never.
// --- User Authentication --------------------------------------------------
```

## Config Directories

### `xxx.d/` — Source-in-Order Fragments

A `conf.d/`-style directory earns its place when **a config has
multiple distinct concerns that share a non-trivial load order**. The
numeric prefix is doing real work — it encodes a dependency that can't
live in alphabetical filenames.

```text
dot_config/bspwm/conf.d/
├── 00-options.sh    # bspc config knobs (must precede rules)
├── 10-colors.sh     # independent of the rest
├── 20-rules.sh      # may reference options
└── 30-autostart.sh  # last; depends on the rest being applied
```

Without that ordering pressure, prefer a single file. Examples in this
repo:

- bspwm — split. Four concerns with real ordering. `.d` earns it.
- sx — single file. Parse-then-dispatch; no tiers.
- qutebrowser — single file. Flat config, no ordering.

### Named Subdirectories Are a Different Pattern

Named subdirectories (e.g., `polybar/bars/`, `polybar/modules/`) encode
a **data model** — one file per bar, one per module — not a load order.
They are not `.d`, and the rule above doesn't constrain them. Reach for
named subdirectories when the config has multiple instances of the same
kind of thing; reach for `.d` when one logical config has multiple
ordering-dependent tiers.

## Per-Language

Formatting and lint rules live in `.editorconfig` and
`.pre-commit-config.yaml`. The sections below capture only what tooling
can't enforce.

### Shell

POSIX-portable conventions. Apply to every `#!/bin/sh` script and every
sourced `.sh` file.

- `set -eu` at the top of every executable script (`-o pipefail` is bash
  only; not portable).
- File-header docstring, templated:

  ```sh
  #!/bin/sh

  # name — one-line purpose ending with period.
  #
  # Section Title:
  #   item       definition-style entry
  #   item       definition-style entry
  #
  # Section Title:
  #   - prose-style bullet entry
  #   - prose-style bullet entry

  set -eu
  ```

  Em dash in the summary line. `#`-only blank lines between sections (the
  docstring reads as one continuous block). Section labels in title case
  with trailing colon. Items indented 3 spaces after the `#`. Item format
  free per section — column-aligned for definitions, `-` bullets for prose.
  All sections after the summary line are optional.

- One-line `#` comment immediately above every function describing what it
  does.
- `readonly NAME='value'` for constants. ALL_CAPS for constant names,
  snake_case for functions and locals.
- Single quotes when no expansion is needed.
- Reach for `awk` for field or line parsing rather than Bash string
  manipulation.
- File-header docstrings use the indented sub-section style above. Setext
  H2 labels apply only to in-code segments, not to the file's opening
  documentation block.

### Bash

Bash is a superset of POSIX shell; every rule under `Shell` applies.
Prefer `#!/bin/sh` unless you specifically need a bash extension.

- Use `[[ ... ]]` over `[ ... ]` for tests. No word-splitting pitfalls,
  supports pattern and regex matching.
- `set -o pipefail` is allowed in addition to `-eu` (it's bash-only).

### Markdown

- Wrap prose at 79 columns (matches `.editorconfig`). Code blocks, URLs, and
  tables are exempt.
- Hyphen `-` for unordered lists; never `*` or `+`.
- ATX headings (`# Title`) for documents. Setext headings are reserved for
  in-code segment labels (see `Labels`).
- Bare URLs in autolinks (`<url>`); named links as `[text](url)`.
- Inline code in `` `backticks` ``.
- Em dash for inline separation, space-padded around the dash.
- Bold uses `**text**` (asterisks); italic uses `_text_` (underscores) —
  matches prettier defaults and avoids visual collision between the two.
  Plain bold for terms, even definitional ones — no italic-and-bold
  combinations.
- Code fences carry a language tag (` ```python `), never bare.

## Vim Modeline

Files whose extension or shebang doesn't disambiguate the language end
with a single trailing line `# vim: ft=<lang>` so vim picks up the
filetype:

```bash
# vim: ft=bash
```

Applies to `.bashrc`, `.bash_profile`, tmux `*.conf`, and similar.
Files whose extension or shebang already disambiguates (`.sh`, `.fish`,
`.py`, `.sxhkdrc`, etc.) skip it.
