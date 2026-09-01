from importlib.metadata import PackageNotFoundError, version

from bro_exchange.bhp import *
from bro_exchange.broxml import *

from .checks import *

try:
    __version__ = version("bro-exchange")
except PackageNotFoundError:
    # Package isn't installed (e.g. running from a source checkout without an install)
    __version__ = "0.0.0.dev0"
