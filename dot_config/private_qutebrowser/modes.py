from _qute_types import ConfigAPI, ConfigContainer

_DEFAULT = ';;'.join(
  [
    'set tabs.show always',
    'set tabs.position top',
    'set tabs.width 15%',
    'set statusbar.show in-mode',
    'set scrolling.bar overlay',
  ]
)
_INFO = ';;'.join(
  [
    'set tabs.show always',
    'set tabs.position left',
    'set tabs.width 250',
    'set statusbar.show always',
  ]
)
_MINIMAL = ';;'.join(
  [
    'set tabs.show never',
    'set statusbar.show in-mode',
    'set scrolling.bar never',
  ]
)


def setup(c: ConfigContainer, config: ConfigAPI) -> None:  # noqa: ARG001
  config.bind('<space>md', _DEFAULT)
  config.bind('<space>mi', _INFO)
  config.bind('<space>mm', _MINIMAL)
