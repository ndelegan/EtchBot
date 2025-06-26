"""
    GUI that allows the use of siglent_driver

    Authors: UIC Chicago Tech Circle Team (Daisy Maldonado)
    Collaborators: Argonne National Laboratory (Nazar Delegan, Clayton Devault)
    Date Created: 06/03/2025
"""

import tkinter as tk
from tkinter import *
from siglent_driver import Siglent

"""
    input_values : sets voltage and current after user
    submits desired inputs

    Args:
        volt_input: User's voltage amount of choice
        curr_input: User's current amount of choice
        sig: Variable which allows calls to functions from siglent_driver 
    Returns:
        Empty return.
    Raises:
        If siglent input is manually altered, synchronization with the GUI will
        be disrupted. Power cycling the device (turning it off and on) is required 
        to restore functionality.
"""
def input_values(volt_input, curr_input, sig):
    # make variables off of user input 
    voltage = float(volt_input.get())
    current = float(curr_input.get())
    # uses siglent_driver functions to set the current and voltage using user input
    sig.set_volt(voltage)
    sig.set_curr(current)


"""
    output_on : turns output on

    Args:
        sig: Variable which allows calls to functions from siglent_driver 
    Returns:
        Empty return.
    Raises:
        No errors. Assumes you are connected correctly.
"""
def output_on(sig, status):
    sig.output_on()
    status.config(text="   Output Status: ON", fg="green")


"""
    output_off : turns output off

    Args:
        sig: Variable which allows calls to functions from siglent_driver 
    Returns:
        Empty return.
    Raises:
        No errors. Assumes you are connected correctly.
"""
def output_off(sig, status):
    sig.output_off()
    status.config(text="   Output Status: OFF", fg="red")


"""
    reset_zero : resets current and voltage to 0

    Args:
        sig: Variable which allows calls to functions from siglent_driver 
    Returns:
        Empty return.
    Raises:
        No errors. Assumes you are connected correctly.
"""
def reset_zero(sig):
    sig.reset_values()


"""
    live_readings : displays current readings of the voltage 
    and the current 

    Args:
        volt: Voltage (V) variable being displayed on screen 
        curr: Current (A) variable being displayed on screen
        sig: Variable which allows calls to functions from siglent_driver 
    Returns:
        Empty return.
    Raises:
        No errors. Assumes you are connected correctly.
"""
def live_readings(volt, curr, sig):
    # uses siglent_driver functions to fet the current and voltage 
    voltage = sig.get_output()[0]
    current = sig.get_current()[0]
    # changes the current and voltage being displayed
    volt.config(text=f"   Voltage: {voltage:.3f} V")
    curr.config(text=f"   Current: {current:.3f} A")


"""
    update_readings : updates voltage (V) and current (A) readings 
    every 0.1 milliseconds

    Args:
        root: Main application window
        volt_lbl: Voltage (V) variable being displayed on screen
        curr_lbl: Current (A) variable being displayed on screen
        sig: Variable which allows calls to functions from siglent_driver
    Returns:
        Empty return.
    Raises:
        No errors. Assumes you are connected correctly.
"""
def update_readings(root, volt_lbl, curr_lbl, sig):
    live_readings(volt_lbl, curr_lbl, sig)
    root.after(100, lambda: update_readings(root, volt_lbl, curr_lbl, sig))


"""
    gui_popup : displays all components of the gui and  
    calls functions for use as necessary

    Args:
        None
    Returns:
        Empty return.
    Raises:
        No errors. Assumes you are connected correctly.
"""
def gui_popup():
    # main window components
    root = tk.Tk()
    root.title("Siglent Power Supply")
    root.geometry("600x350")
    sig = Siglent()

    # --- set values section of GUI --- 
    values_frame = tk.LabelFrame(root, text="Set Values", padx=10, pady=10)
    values_frame.pack(anchor = "w")
     # voltage prompts and input boxes
    volt_lbl = Label(values_frame, text = "   Voltage (V):")
    volt_lbl.pack(side=LEFT)
    volt_input = Entry(values_frame, width=10)
    volt_input.pack(side=LEFT, padx=15) 
     # current prompts and input boxes
    curr_lbl = Label(values_frame, text = "  Current (A):")
    curr_lbl.pack(side=LEFT)
    curr_input = Entry(values_frame, width=10)
    curr_input.pack(side=LEFT, padx=15) 
     # button to set values
    vals_btn = tk.Button(values_frame, text="Set Values", command=lambda: input_values(volt_input, curr_input, sig))
    vals_btn.pack(padx=15, pady=20)


    # --- control buttons section of GUI ---
    controls_frame = Frame(root)
    controls_frame.pack(anchor = "w")
    
    output_status = Label(controls_frame, text="   Output Status: OFF", fg="red")
    output_status.pack(side=LEFT, padx=10)

    on_btn = tk.Button(controls_frame, text="Output On", command=lambda: output_on(sig, output_status)) # output on button
    on_btn.pack(padx=15, pady=20, side=LEFT)

    off_btn = tk.Button(controls_frame, text="Output Off", command=lambda: output_off(sig, output_status)) # output off button
    off_btn.pack(padx=15, pady=20, side=LEFT)

    reset_btn = tk.Button(controls_frame, text="Reset Input to 0", command=lambda: reset_zero(sig)) # reset to 0 button
    reset_btn.pack(padx=15, pady=20, side=LEFT)


    # --- live readings section of GUI ---
    readings_frame = tk.LabelFrame(root, text="Live Readings:", padx=10, pady=10)
    readings_frame.pack(anchor = "w")

    volt_lbl = Label(readings_frame, text = "   Voltage: -- V")
    volt_lbl.pack(side=LEFT)

    curr_lbl = Label(readings_frame, text = "   Current: -- A")
    curr_lbl.pack(side=LEFT)
    update_readings(root, volt_lbl, curr_lbl, sig)

    # Run the app
    root.mainloop()

if __name__ == "__main__":
    gui_popup()