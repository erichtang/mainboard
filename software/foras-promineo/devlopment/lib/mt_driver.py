from micropython import const
from adafruit_bus_device.i2c_device import I2CDevice

class mt_driver_simulated:
    def __init__(self, device, send_result_of_simulation):
        self.send_result_of_simulation = send_result_of_simulation
        self.send_result_of_simulation(device, "initialized")
        self.device = device

    def stop(self):
        self.send_result_of_simulation(self.device, 'reset')
    
    def set_level(self, outputnum, level):
        self.send_result_of_simulation(self.device, str(outputnum) + " set to " + str(level))


# addresses that the driver can be
possible_i2c_address = [0x58, 0x59, 0x5A, 0x5B, 0x5C, 0x5D, 0x5E, 0x5F, 0x60, 0x61]

# Define the flags for  the device
# SCMD_STATUS_1 bits
SCMD_ENUMERATION_BIT       = const(0x01)
SCMD_BUSY_BIT              = const(0x02)
SCMD_REM_READ_BIT          = const(0x04)
SCMD_REM_WRITE_BIT         = const(0x08)

# Address map
SCMD_ID                    = const(0x01)
SCMD_MA_DRIVE              = const(0x20)


SCMD_DRIVER_ENABLE         = const(0x70)
SCMD_STATUS_1              = const(0x77)


class mt_driver():
    """
    initializes the class

    Inputs: address -> the address of the driver board
            i2c -> an busio.I2C object that the driver board is connected to, MUST BE LOCKED

    Outputs: NONE
    """
    def __init__(self, address, i2c_bus):
        # makes sure the address is possible for the device, if not raises an exception
        if address not in possible_i2c_address:
            raise TypeError("Invalid Address for Driver")
        else:
            # setting some attributes
            #self._address = address
            self.i2c_device = I2CDevice(i2c_bus, address)
            self._buf = bytearray(2)

            # configure the I2C device
            self._begin()
            self._enable()

    """
    reads one byte of data from register at the inputted address

    Inputs: register_address -> the address of the register in the device

    Outputs: the data from the register in a bytes object
    """
    def _readByte(self, register_address):
        with self.i2c_device as i2c:
            i2c.write(bytes([register_address]))
        return self._buf[0]

    """
    writes one byte of data to the register at the inputted address

    Inputs: register_address -> the address of the register in the device
            value -> the value to write to the register, must an int or bytes object, with size of one byte
    Outputs: NONE
    """
    def _writeByte(self, register_address, value):
        self._buf[0] = register_address
        self._buf[1] = value
        with self.i2c_device as i2c:
            i2c.write(self._buf)
		

    def _begin(self):
        """
            Initialize the operation of the SCMD module
            :return: Returns true of the initializtion was successful, otherwise False.
            :rtype: bool
        """
        # dummy read
        self._readByte(SCMD_ID)

        return self._readByte(SCMD_ID)


    # check if enumeration is complete
    def _ready(self):
        """
            Returns if the driver is ready
            :return: Ready status
            :rtype: boolean
        """
        statusByte = self._readByte(SCMD_STATUS_1)

        return statusByte & SCMD_ENUMERATION_BIT  and  statusByte != 0xFF  #wait for ready flag and not 0xFF


    def _busy(self):
        """
            Returns if the driver is busy
            :return: busy status
            :rtype: boolean
        """
        statusByte = self._readByte(SCMD_STATUS_1)

        return statusByte & (SCMD_BUSY_BIT | SCMD_REM_READ_BIT | SCMD_REM_WRITE_BIT) != 0

    # Enable and disable functions.  Call after begin to enable the h-bridges
    def _enable(self):
        """
            Enable driver functions
            :return: No return value
        """
        self._writeByte(SCMD_DRIVER_ENABLE, 0x01)


    def _disable(self):
        """
            Disable driver functions
            :return: No return value
        """
        self._writeByte(SCMD_DRIVER_ENABLE, 0x00)


    """
    stops the operation of the driver board and resets all registers in it

    Inputs: NONE

    Outputs: NONE
    """
    def stop(self):
        # reseting all outputs to not output anything
        for i in range(34):
            self._writeByte(SCMD_MA_DRIVE + i, 0x80)

        # disabling the driver
        self._disable()

    #
    #   outputNum -- output number from 0 to 33
    #   level -- 0 to 127 for drive strength
    def set_level(self, outputNum, level):
        # Make sure the motor number is valid
        if outputNum < 34:
            level+=128
            self._writeByte(SCMD_MA_DRIVE + outputNum, level)