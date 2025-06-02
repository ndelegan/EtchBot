import tkinter as tk
from tkinter import *
from siglent_driver import Siglent
# Function to run when "Set Values" button is clicked
def input_values():
    voltage = float(volt_input.get())
    current = float(curr_input.get())
    sig.set_volt(voltage)
    sig.set_curr(current)
    # voltage = sig.set_volt(volt_input.get())
    # current = sig.set_curr(curr_input.get())
    # voltage = volt_input.get()
    # current = curr_input.get()
    # print (f"Voltage: {voltage} V\nCurrent: {current} A")
def output_on():
    sig.output_on()
    # print("on")
def output_off():
    sig.output_off()
    # print("off")
def reset_zero():
    sig.reset_values()
    # print("redone")
def live_readings(volt, curr):
  
    # volt.config(text=f"Voltage: {volt} V")
    # curr.config(text=f"Current: {curr} A")
    voltage = sig.get_output()[0]
    current = sig.get_current()[0]
    volt.config(text=f"   Voltage: {voltage:.3f} V")
    curr.config(text=f"   Current: {current:.3f} A")
    
def update_readings():
    live_readings(volt_lbl, curr_lbl)
    root.after(1000, update_readings)
# main window
root = tk.Tk()
root.title("Siglent Power Supply")
root.geometry("600x350")
sig = Siglent()
# Main Menu 
lbl = Label(root, text = "Set Values: ")
lbl.pack(anchor = "w")
# set values
values_frame = Frame(root)
values_frame.pack(anchor = "w")
volt_lbl = Label(values_frame, text = "   Voltage (V):")
volt_lbl.pack(side=LEFT)
volt_input = Entry(values_frame, width=10)
volt_input.pack(side=LEFT, padx=15) 
curr_lbl = Label(values_frame, text = "  Current (A):")
curr_lbl.pack(side=LEFT)
curr_input = Entry(values_frame, width=10)
curr_input.pack(side=LEFT, padx=15) 
vals_btn = tk.Button(values_frame, text="Set Values", command=input_values)
vals_btn.pack(padx=15, pady=20)
# control buttons
controls_frame = Frame(root)
controls_frame.pack(anchor = "w")
on_btn = tk.Button(controls_frame, text="Output On", command=output_on)
on_btn.pack(padx=15, pady=20, side=LEFT)
off_btn = tk.Button(controls_frame, text="Output Off", command=output_off)
off_btn.pack(padx=15, pady=20, side=LEFT)
reset_btn = tk.Button(controls_frame, text="Reset to 0", command=reset_zero)
reset_btn.pack(padx=15, pady=20, side=LEFT)
# live readings
readings_frame = Frame(root)
readings_frame.pack(anchor = "w")
lbl = Label(readings_frame, text = "Live Readings: ")
lbl.pack(anchor = "w", pady=20)
volt_lbl = Label(readings_frame, text = "   Voltage: -- V")
volt_lbl.pack(side=LEFT)
curr_lbl = Label(root, text = "   Current: -- A")
curr_lbl.pack(side=LEFT)
# live_readings(volt_lbl, curr_lbl)
update_readings()
# Run the app
root.mainloop()