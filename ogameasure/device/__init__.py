from .SCPI import scpi_common

from . import Agilent
from . import Agilent as Keysight
from . import Anritsu
from . import Cosmotechs
from . import ELVA1
from . import HEIDENHAIN
from . import KIKUSUI
from . import Lakeshore
from . import OrientalMotor
from . import Pfeiffer
from . import Phasematrix
from . import SENA
from . import TandD

try:
    from . import Canon
except ImportError:
    print(
        "You can't import device.Canon.M100_raspi "
        "because there isn't gphoto2 package."
    )
    print(
        "Please install `libgphoto2` (C language package)"
        "and run `pip install gphoto2`"
    )
    pass
