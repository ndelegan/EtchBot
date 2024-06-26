"""

    Python class called "Siglent" to control the Siglent SPS5161x device.

    Authors: UIC Chicago Tech Circle Team (Lisset Rico, Lisette Ruano, Aima Quibuddin)
    Collaborators: Argonne National Laboratory (Nazar Delegan, Clayton Devault)
    Date Created: 06/20/2024

"""

import pyvisa
import time

"""Siglent Class

    Functions:
        __init__ : connect to device
        set_volt : set device voltage
        set_curr : set device current
        output_on : turn on voltage output
        output_off : turn off voltage output
        get_ouput : return current voltage output
        reset_values : set voltage and current to 0
        close : closes connection to device

"""

class Siglent:
    """
        __init__ : connect to device

        Args:
            self: class object
        Returns:
            Empty return.
        Raises:
            Exception. Prints error if can't connect to device.
    """
    def __init__(self):
        rm = pyvisa.ResourceManager() # finds all available devices
        print(rm.list_resources()) # prints out an array list of all available devices

        try:
          device_str = 'USB0::0XF4EC::0X1452::SPS61ABQ7R0361::INSTR'
          self.device = rm.open_resource(device_str) # connects directly to siglent device
          print("Connected: ", self.device.query("*IDN?")) # prints siglents basic info(name, ip, etc)
        except Exception as err:
          print("Cannot connect to Siglent: ", err)


    """
        set_volt : set device voltage

        Args:
            self: class object
            volt: integer
        Returns:
            Empty return.
        Raises:
            No errors. Assumes you are connected correctly.
    """
    def set_volt(self, volt:int):
        str_volt = "VOLT " + str(volt)
        self.device.write(str_volt)


    """
        set_curr : set device current

        Args:
            self: class object
            curr: integer
        Returns:
            Empty return.
        Raises:
            No errors. Assumes you are connected correctly.
    """
    def set_curr(self, curr:int):
        str_curr = "CURR " + str(curr)
        self.device.write(str_curr)


    """
        output_on : turn on voltage output

        Args:
            self: class object
        Returns:
            Empty return.
        Raises:
            No errors. Assumes you are connected correctly.
    """
    def output_on(self):
        self.device.write("OUTP 1")


    """
        output_off : turn off voltage output

        Args:
            self: class object
        Returns:
            Empty return.
        Raises:
            No errors. Assumes you are connected correctly.
    """
    def output_off(self):
        self.device.write("OUTP 0")


    """
        get_ouput : return current voltage output

        Args:
            self: class object
        Returns:
            Returns a array with one value.
        Raises:
            No errors. Assumes you are connected correctly.
    """
    def get_output(self):
        return self.device.query_ascii_values("MEAS:VOLT?")


    """
        reset_values : set voltage and current to 0

        Args:
            self: class object
        Returns:
            Empty return.
        Raises:
            No errors. Assumes you are connected correctly.
    """
    def reset_values(self):
        self.device.write("VOLT 0")
        self.device.write("CURR 0")


    """
        close : closes connection to device

        Args:
            self: class object
        Returns:
            Empty return.
        Raises:
            No errors. Assumes you are connected correctly.
    """
    def close(self):
        self.device.close()
