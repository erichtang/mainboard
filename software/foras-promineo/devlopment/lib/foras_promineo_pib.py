"""
foras_promineo_pib.py
====================================================================
Foras Promineo mission-specific payload interface board library
    this board also has the mt drivers, irridium, and other things
only pertains to the pib, see foras_promineo_payload.py for things on the payload.

* Authors C. Hillis
4/6
====================================================================

"""

class PIB():

    def __init__(self, satellite):
        """
        inherits superclass satellite from pycubed.py
        init's FP pib devices and any functionality for managing them.
        """
        super.__init__(satellite)

        self.hardware = {
            'io_expander' : False,
            'dac' : False,
            'adc' : False,
            'irridium' : False,
            #other pib devices here
        }

        ### this currently has nothing, but will change as the dev process foes on.

    def reinit(self): ## call this in satellite.reinit
        pass

    def powermode(self, mode): ## call this in satellite.reinit
        pass
