try:
    from importlib.metadata import version
except ImportError:
    from importlib_metadata import version

try:
    __version__ = version("ogameasure")
except:
    __version__ = "0.0.0"


from .communicator import *
from .device import *
