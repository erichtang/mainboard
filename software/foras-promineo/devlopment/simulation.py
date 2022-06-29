"""
simulation class

add description
"""

import usb_cdc

class Simulation():

    def __init__(self, satellite):
        """
        Init routine for this class
        """
        self.cubesat = satellite

        #dict that stores bools for indicating if this value is simulated or not. default all are false.
        self.simulate = {
            'value1' : False,
        }

    """
    function to ask host for simulated value with given inputs
    may need to be changed to be a property to play nice 
    """
    def ask_for_value(self, value, *args):
        pass


    """
    THIS IS EXAMPLE CODE FOR HOW I IMAGINE THIS WILL BE USED IN OTHER FILES
    """
    """
    def foo(self, a, b ,c):
        if self.cubesat.sim.simulate['value1']:
            return(self.cubesat.sim.ask_for_value('value1', a,b,c))
        else:
            #regular computation of variable
            pass
    """