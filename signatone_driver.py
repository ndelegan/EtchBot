"""

    Python class called "Signatone" to control the Signatone CAP-946 devices.

    Authors: UIC Chicago Tech Circle Team (Claudia Jimenez, Lisset Rico)
    Collaborator(s): Argonne National Laboratory (Nazar Delegan, Clayton Devault)
    Date Created: 06/20/2024

    To-Do:
    - Test the functions

"""

import pyvisa
from pyvisa import constants
import time

"""
    Signatone Class

    Functions:
        __init__ : connect to device
        set_home : This sets the current X, Y position of the active device to 0,0
        set_device : Select the active device for future commands.
        move_rel : Moves the current device to the new position in reference to the current position.
        move_z : Moves the current selected device to the new absolute Z position in reference to the current Z position.
        move_xyz : Move the current CAP or the microscope to the specified x, y, z location, or the stage to the specified x, y, z location.
        save_image : Save the current camera image to the specified file.
        get_scope : Returns the current X, Y, Z position of the microscope.
        abort_motion : Abort motion of the current device
        default_settings : Sets all devices to a 0,0 setting.
        close : closes connection to device

"""

class Signatone:
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
          device_str = 'TCPIP0::124.51.29.30::9090::SOCKET'
          self.device = rm.open_resource(device_str) # connects directly to siglent device
          self.device.read_termination = '\n'
          self.device.write_termination = '\n'
          # set termination method attributes 
          self.device.set_visa_attribute(constants.VI_ATTR_SUPPRESS_END_EN, constants.VI_FALSE)
          self.device.set_visa_attribute(constants.VI_ATTR_SEND_END_EN, constants.VI_TRUE)
          self.device.set_visa_attribute(constants.VI_ATTR_TERMCHAR_EN, constants.VI_TRUE)
          self.device.set_visa_attribute(constants.VI_ATTR_FILE_APPEND_EN, constants.VI_FALSE)
          self.device.query('*IDN?')
          print("Connected: ", self.device.query("*IDN?")) # prints siglents basic info(name, ip, etc)
        except Exception as err:
          print("Cannot connect to Signatone: ", err)
          quit()


    """
        set_home : This sets the current X, Y position of the active device to 0,0

        Args:
            self: class object
        Returns:
            Empty return.
        Raises:
            Exception. Prints error if can't connect to device.
    """
    def set_home(self):
        self.device.query("SETHOME")


    """
        set_device : Select the active device for future commands.

        Args:
            self: class object
            dev: string parameter
        Returns:
            Empty return.
        Raises:
            Exception. Prints error if can't connect to device.
    """
    def set_device(self, dev):
        device_str = "SETDEVICE " + dev
        self.device.query(device_str)
    """
    get_cap : returns the current x,y,z position of the active device in microns

    Args:
        None
    Returns:
        x,y,z coordinatinates
    Raises: 
        Exception. Prints error if can't connect to device.
    """
    def get_cap(self):
        device_str = "GETCAP"
        position = self.device.query(device_str)
        return position
    """
        move_rel : Moves the current device to the new position in reference to the current position.

        Args:
            self: class object
            x: int parameter
            y: int parameter
        Returns:
            Empty return.
        Raises:
            Exception. Prints error if can't connect to device.
    """
    def move_rel(self, x, y):
        move = "MOVEXREL " + x + " " + y
        self.device.query(move)


    """
        move_z : Moves the current selected device to the new absolute Z position in reference to the current Z position.

        Args:
            self: class object
            amn: int parameter
        Returns:
            Empty return.
        Raises:
            Exception. Prints error if can't connect to device.
    """
    def move_z(self, amn):
        z = "MOVEZREL " + amn
        self.device.query(z)


    """
        move_xyz : Move the current CAP or the microscope to the specified x, y, z location, or the stage to the specified x, y, z location.

        Args:
            self: class object
            x: int parameter
            y: int parameter
            z: int parameter
        Returns:
            Empty return.
        Raises:
            Exception. Prints error if can't connect to device.
    """
    def move_xyz(self, x, y, z):
        xyz = "MOVEXYZABS " + x + " " + y + " " + z
        self.device.query(xyz)


    """
        save_image : Save the current camera image to the specified file.

        Args:
            self: class object
            path: string parameter
        Returns:
            Empty return.
        Raises:
            Exception. Prints error if can't connect to device.
    """
    def save_image(self, path):
        save = "SAVEIMAGE " + path
        self.device.query(save)


    """
        get_scope : Returns the current X, Y, Z position of the microscope.

        Args:
            self: class object
        Returns:
            Current x, y, z location of the microscrope as an array.
        Raises:
            Exception. Prints error if can't connect to device.
    """
    def get_scope(self):
        return self.device.query("GETSCOPE")


    """
        abort_motion : Abort motion of the current device

        Args:
            self: class object
        Returns:
            Empty return.
        Raises:
            Exception. Prints error if can't connect to device.
    """
    def abort_motion(self):
        self.device.query("ABORTMOTION")


    """
        default_settings : Sets all devices to a 0,0 setting.

        Args:
            self: class object
        Returns:
            Empty return.
        Raises:
            Exception. Prints error if can't connect to device.
    """
    def default_settings(self):
        self.device.query("SETDEVICE SCOPE")
        self.device.query("MOVEXYZABS ") # get instrument measurements

        self.device.query("SETDEVICE CAP1")
        self.device.query("MOVEXYZABS ") # get instrument measurements

        self.device.query("SETDEVICE CAP4")
        self.device.query("MOVEXYZABS ") # get instrument measurements



    """
        close : closes connection to device

        Args:
            self: class object
        Returns:
            Empty return.
        Raises:
            Exception. Prints error if can't connect to device.
    """
    def close(self):
        self.device.close()
