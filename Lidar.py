from smbus2 import *
import time

DEFAULT_ADDRESS = 0x62 # Address of the device
#Internal registers
ACQ_COMMAND = 0x00 # W: 0x00 Reset all registers to default
                   # W: 0x03 Measure distance (no correction)
                   # W: 0x04 Measure distance (Bias correction)
STATUS = 0x01 # R: Status register of the device
DISTANCE_OUTPUT = 0x8f # R: Distance measurement in cm (2 Bytes)

"""
Interface for the Garmin Lidar-Lite v3
"""
class Lidar:
    def __init__(self):
        self.bus = SMBus(1)

    """ 
    Take one measurement in cm
    @:param: bias_correction boolean, determines if measurement uses bias correction or not
    @:return int distance in cm
    """
    def read_distance(self, bias_correction=True):
        if bias_correction:
            # Write 0x04 to 0x00 for bias corrected measurement
            self.bus.write_byte_data(DEFAULT_ADDRESS, ACQ_COMMAND,0x04)
        else:
            # Write 0x03 to 0x00 for no bias correction
            self.bus.write_byte_data(DEFAULT_ADDRESS, ACQ_COMMAND, 0x03)

        # Wait for device to receive distance reading
        while self.device_busy():pass
        # Read HIGH and LOW distance registers
        distance = self.bus.read_i2c_block_data(DEFAULT_ADDRESS, DISTANCE_OUTPUT, 2)
        return distance[0] << 8 | distance[1] # combine both bytes

    """
    Read the STATUS register
    :return: list of ints
        bit 6: Process error flag
        bit 5: Health flag
        bit 4: Secondary return flag
        bit 3: Invalid signal flag
        bit 2: Signal overflow flag
        bit 1: Reference overflow flag
        bit 0: Busy flag
    """
    def device_status(self):
        # Read the STATUS register, bits 0-6 only
        current_config = int(self.bus.read_byte_data(DEFAULT_ADDRESS, STATUS))
        # Convert to binary, fill rest with 0's
        current_config = bin(current_config)[2:].zfill(7)
        return [int(bit) for bit in str(current_config)]

    """
    Check if the device is busy
    @:return boolean, true = busy
    """
    def device_busy(self):
        # STATUS register bit 0 represents busy flag, 0 for ready, 1 for busy
        return self.device_status()[-1]

