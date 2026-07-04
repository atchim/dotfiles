#!/bin/sh

# Enable corepack so pnpm and yarn are served as corepack-managed shims in the
# npm prefix's bin (~/.local/npm/bin, placed on PATH by .bash_profile). Gentoo's
# nodejs doesn't bundle corepack, so install it as an npm global first when it's
# missing. `corepack enable` only writes shim files (version download happens
# lazily on first pnpm/yarn use), so this is offline-safe and idempotent.

set -eu

if ! command -v npm >/dev/null 2>&1; then
  printf 'enable-corepack: npm not installed; skipping.\n' >&2
  exit 0
fi

# Match the prefix .bash_profile exports, independent of the ambient env.
: "${NPM_CONFIG_PREFIX:=${HOME}/.local/npm}"
export NPM_CONFIG_PREFIX

# corepack lives in (and writes its shims into) the prefix bin; it must be on
# PATH for `corepack enable` to locate itself.
PATH="${NPM_CONFIG_PREFIX}/bin:${PATH}"
export PATH

if ! command -v corepack >/dev/null 2>&1; then
  npm install -g corepack
fi

corepack enable
