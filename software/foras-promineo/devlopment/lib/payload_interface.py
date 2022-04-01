"""
CircuitPython driver for foras promineo PIB.
PyCubed Hardware Version: mainboard-v5-SLI
CircuitPython Version: 7.0.0 alpha
Library Repo: 

* Author(s): Marek Brodke, C. Hillis

To-Do
    1. Get IMU up and running, in this lib and it's own lib
    2. get magnetotorquer driver up and running

"""
        
        
        
        
        
        
        
        """
        # ------------------------------------------ Start Section v -- move tbis to a PIB library?

        # initializing magneto torquer driver board connection 
        try:
            # initializing the driver board at the address 0x58 on the i2c bus
            if not self.simulation:
                pass
                #self.driver_x = mt_driver(0x58, self.i2c1)
                #self.driver_y = mt_driver(0x59, self.i2c1)
                #self.driver_z = mt_driver(0x60, self.i2c1)
            else:
                self.driver_x = mt_driver_simulated(0x58, self.send_result_of_simulation)
                self.driver_y = mt_driver_simulated(0x59, self.send_result_of_simulation)
                self.driver_z = mt_driver_simulated(0x60, self.send_result_of_simulation)

            self.hardware['MTDRIVERS'] = True
        
        except Exception as e:
            self.error_encountered = True
            self.log('[WARNING][MT_DRIVER]:' + str(e))

        # ------------------------------------------ End Section ^
        """