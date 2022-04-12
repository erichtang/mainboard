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
        inherits superclass satellite from pycubed.py
        init's FP payload devices and any functionality for managing it.
        """
        self.cubesat = satellite

        self.hardware = {
            'openMV' : False,
            #other payload devices here
        }

        ### this currently has nothing, but will change as the dev process foes on.

    def reinit(self): ## call this in satellite.reinit
        pass

    def powermode(self, mode): ## call this in satellite.reinit
        pass
