import importlib
import sys

from qutebrowser.config.config import ConfigContainer
from qutebrowser.config.configfiles import ConfigAPI

config: ConfigAPI = config  # type: ignore[used-before-def]  # noqa: F821
c: ConfigContainer = c  # type: ignore[used-before-def]  # noqa: F821

config.load_autoconfig(False)

_DOMAINS = (
  'completion',
  'content',
  'pages',
  'search',
  'session',
  'statusbar',
  'tabs',
  'modes',
  'oil8',
)

for _name in _DOMAINS:
  if _name in sys.modules:
    _mod = importlib.reload(sys.modules[_name])
  else:
    _mod = importlib.import_module(_name)
  if _name == 'oil8':
    _mod.draw(c)
  else:
    _mod.setup(c, config)

config.bind('<space>rr', 'config-source')
