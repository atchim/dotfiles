from _types import ConfigAPI, ConfigContainer


def setup(c: ConfigContainer, config: ConfigAPI) -> None:  # noqa: ARG001
  c.statusbar.show = 'in-mode'
