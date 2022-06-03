"""
foras_promineo_payload.py
====================================================================
Foras Promineo mission-specific payload library
only pertains to the payload, see foras_promineo_pib.py for things on the PIB.

* Authors C. Hillis
4/6
====================================================================

"""

class payload():

    def __init__(self, satellite):
        """
        inherits satellite from pycubed.py
        """
        self.cubesat = satellite

        self.hardware = {
            'OPENMV' : False,
            #other payload devices here
        }

    def powermode(self, mode): ## call this in satellite.reinit
        pass
