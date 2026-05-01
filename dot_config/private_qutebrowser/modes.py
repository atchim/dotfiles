from _types import ConfigAPI, ConfigContainer

_DEFAULT = (
  'set tabs.show always ;; '
  'set tabs.position top ;; '
  'set tabs.width 15% ;; '
  'set statusbar.show in-mode ;; '
  'set scrolling.bar when-searching'
)
_INFO = (
  'set tabs.show always ;; '
  'set tabs.position left ;; '
  'set tabs.width 250 ;; '
  'set statusbar.show always'
)
_MINIMAL = (
  'set tabs.show never ;; '
  'set statusbar.show in-mode ;; '
  'set scrolling.bar never'
)


def setup(c: ConfigContainer, config: ConfigAPI) -> None:  # noqa: ARG001
  config.bind('<space>md', _DEFAULT)
  config.bind('<space>mi', _INFO)
  config.bind('<space>mm', _MINIMAL)
