# Dotfiles

Personal dotfiles managed with [chezmoi](https://chezmoi.io).

## Managed configs

- **Bash** — `~/.bash_profile`, `~/.bashrc`
- **Alacritty** — `~/.config/alacritty/alacritty.toml`

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
- [Starship](https://starship.rs)

## Installation

```sh
chezmoi init --apply atchim
```

Enable pre-commit hooks after cloning:

```sh
pre-commit install
```
