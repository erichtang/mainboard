"""
top level adcs implementation
"""

from .interface import Interface
from . import cdh
from . import manager
from .types import status_t, state_t


class ADCS:

    # Physical Constants
    EPOCH = 2459580.5 # temporary

    pi = 3.14159265358979323846
    rho = 3.986004418e14 # m^3/s^2

    # Implementation Constants
    MAX_ATTEMPTS = 4

    def __init__(self, satellite):

        self.cubesat = satellite

        # ADCS data variables
        self.status = status_t.ERROR
        self.state = state_t.Safe1
            # and many more.....








        
        