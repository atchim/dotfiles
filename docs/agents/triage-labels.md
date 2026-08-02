# Triage labels

The skills speak in terms of five canonical triage roles. This file maps
those roles onto the label strings actually used in this repo's tracker,
GitHub Issues on `atchim/dotfiles`.

| Role in mattpocock/skills | Label in our tracker | Meaning                                  |
| ------------------------- | -------------------- | ---------------------------------------- |
| `needs-triage`            | `needs-triage`       | Maintainer needs to evaluate this issue  |
| `needs-info`              | `needs-info`         | Waiting on reporter for more information |
| `ready-for-agent`         | `ready-for-agent`    | Fully specified, ready for an AFK agent  |
| `ready-for-human`         | `ready-for-human`    | Requires human implementation            |
| `wontfix`                 | `wontfix`            | Will not be actioned                     |

The defaults are kept as-is — every label string equals its role name.
`wontfix` is GitHub's stock label, reused rather than duplicated; the
other four were created for this repo.

When a skill names a role, such as "apply the AFK-ready triage label",
use the corresponding string from the right-hand column. Apply and remove
them with `gh issue edit <n> --add-label` and `--remove-label`; see
`docs/agents/issue-tracker.md`.

Edit the right-hand column to match whatever vocabulary you actually use.
Changing a string here does not rename the label on GitHub — do that with
`gh label edit`, or the two drift apart.
