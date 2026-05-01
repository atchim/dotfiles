from _types import ConfigAPI, ConfigContainer


def setup(c: ConfigContainer, config: ConfigAPI) -> None:  # noqa: ARG001
  c.content.pdfjs = True
  c.spellcheck.languages = ['en-US', 'pt-BR']
