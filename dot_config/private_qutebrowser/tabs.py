from _types import ConfigAPI, ConfigContainer


def setup(c: ConfigContainer, config: ConfigAPI) -> None:
  c.tabs.position = 'top'
  c.tabs.show = 'always'
  config.bind('<space>tp', 'config-cycle tabs.position top left')
  config.bind('<space>tt', 'config-cycle tabs.show always never switching')
