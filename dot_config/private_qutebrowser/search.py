from _types import ConfigAPI, ConfigContainer


def setup(c: ConfigContainer, config: ConfigAPI) -> None:  # noqa: ARG001
  c.url.searchengines = {
    'DEFAULT': 'https://google.com/search?q={}',
    '#': 'https://www.color-name.com/hex/{}',
    'a': 'https://wiki.archlinux.org/index.php?search={}',
    'cor': 'https://rastreamento.correios.com.br/app/index.php?objetos={}',
    'd': 'https://duckduckgo.com/?q={}',
    'dblp': 'https://dblp.org/search?q={}',
    'dpl': 'https://www.deepl.com/translator#au/au/{}',
    'g': 'https://www.google.com/search?q={}',
    'gb': 'https://gentoobrowse.randomdan.homeip.net/search?criteria={}',
    'gbp': 'https://gentoobrowse.randomdan.homeip.net/packages/{}',
    'gf': 'https://packages.gentoo.org/useflags/{}',
    'gh': 'https://github.com/search?q={}',
    'gh/': 'https://github.com/{}',
    'gi': 'https://www.google.com/search?tbm=isch&q={}',
    'gm': 'https://meet.google.com/{}',
    'gt': 'https://translate.google.com/?sl=auto&text={}',
    'gw': 'https://wiki.gentoo.org/index.php?search={}',
    'mdn': 'https://developer.mozilla.org/en-US/search?q={}',
    'pc-jira': 'https://precocerto.atlassian.net/browse/PC-{}',
    'rs': 'https://doc.rust-lang.org/std/index.html?search={}',
    'rsc': 'https://docs.rs/releases/search?query={}',
    'sc': 'https://soundcloud.com/search?q={}',
    'sci': 'https://sci-hub.se/{}',
    'w': 'https://wikipedia.org/w/index.php?search={}',
    'wbm': 'https://web.archive.org/web/*/{}',
    'y': 'https://www.youtube.com/results?search_query={}',
    'z': 'http://gpo.zugaina.org/Search?search={}',
  }
