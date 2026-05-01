from _types import ConfigAPI, ConfigContainer


def setup(c: ConfigContainer, config: ConfigAPI) -> None:  # noqa: ARG001
  c.url.default_page = 'https://www.google.com'
  c.url.start_pages = 'https://www.google.com'
