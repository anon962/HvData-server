from pathlib import Path
from urlpath import URL

# file urls
ROOT_DIR = Path(__file__).parent.parent

CONFIG_DIR = ROOT_DIR / 'config'
DATA_DIR = ROOT_DIR / 'data'


# hv urls
HV_ROOT = URL('http://alt.hentaiverse.org')

HV_BAZAAR = HV_ROOT.add_query(s='Bazaar')

HV_LOTTO_WEAPON = HV_BAZAAR.add_query(ss='lt')
HV_LOTTO_ARMOR = HV_BAZAAR.add_query(ss='la')


# other urls
FORUM_ROOT = URL('https://forums.e-hentai.org/index.php')
SUPER_ROOT = URL('https://reasoningtheory.net')

SUPER_LIST = SUPER_ROOT / 'itemlist'
SUPER_LOG = SUPER_ROOT / 'bidlog'
SUPER_TIMES = SUPER_ROOT / 'bidtimes'