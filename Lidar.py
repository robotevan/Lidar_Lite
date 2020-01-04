from smbus2 import *
import time

DEFAULT_ADDRESS = 0x62 # Address of the device
#Internal registers
ACQ_COMMAND = 0x00 # W: 0x00 Reset all registers to default
                   # W: 0x03 Measure distance (no correction)
                   # W: 0x04 Measure distance (Bias correction)
STATUS = 0x01
DISTANCE_OUTPUT = 0x8f # Distance measurement in cm (2 Bytes)

"""
Interface for the Garmin Lidar-Lite v3
"""
class Lidar:
    def __init__(self):
        self.bus = SMBus(1)

    def measure_distance(self, bias_correction=True):
        if bias_correction:
            # Write 0x04 to 0x00 for bias corrected measurement
            self.bus.write_byte_data(DEFAULT_ADDRESS, ACQ_COMMAND,0x04)
        else:
            # Write 0x03 to 0x00 for no bias correction
            self.bus.write_byte_data(DEFAULT_ADDRESS, ACQ_COMMAND, 0x03)
        # Wait and read 16 bits from the distance register
        time.sleep(0.02)
        distance = self.bus.read_i2c_block_data(DEFAULT_ADDRESS, DISTANCE_OUTPUT, 2)
        time.sleep(0.02)
        print(distance[0] << 8 | distance[1])
