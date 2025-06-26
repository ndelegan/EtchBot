"""
    GUI that allows the use of etching

    Authors: UIC Chicago Tech Circle Team (Daisy Maldonado)
    Collaborators: Argonne National Laboratory (Nazar Delegan, Clayton Devault)
    Date Created: 06/23/2025
"""
from tkinter import *
import tkinter as tk
import threading
from signatone_driver import Signatone
from siglent_gui import gui_popup as launch_siglent_gui
from etching_main import full_grid_etch as begin_full_etch

"""
    start_siglent : Launches the Siglent GUI in a separate thread.

    Args:
        None
    Returns:
        Empty return.
    Raises:
        No errors. Assumes you are connected correctly.
"""
def start_siglent():
    threading.Thread(target=launch_siglent_gui).start()
    
    
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
    # open root window 
    root = Tk()
    root.title("Welcome to Etch Bot!")
    root.geometry('600x350')
    start_siglent() # open siglent GUI
    
    # Variables which will later assist in the arguments for calling begin_full_etch (full_grid_etch)
    mem_var = StringVar()
    row_mem_var = StringVar()
    street_var = StringVar()
    grid_len_var = StringVar()
    x_ul_var = StringVar()
    y_ul_var = StringVar()
    z_ul_1_var = StringVar()
    z_ul_4_var = StringVar()
    x_ur_var = StringVar()
    y_ur_var = StringVar()
    z_ur_1_var = StringVar()
    z_ur_4_var = StringVar()
    x_ll_var = StringVar()
    y_ll_var = StringVar()
    z_ll_1_var = StringVar()
    z_ll_4_var = StringVar()
    z_t_1_var = StringVar()
    z_t_4_var = StringVar()
    z_e_4_var = StringVar()
    z_e_1_var = StringVar()
    
    
    """
        create_labeled_entry : Creates a labeled entry field in a frame for user inputs

        Args:
            root: The parent widget where the entry field will be added
            label_prompt: The text prompt displayed next to the input box
            var: The variable where the input will be stored
            callback: A function to be called when Enter is pressed.
        Returns:
            A tuple containing the frame and entry widget
        Raises:
            No errors. Assumes you are connected correctly.
    """
    def create_labeled_entry(root, label_prompt, var, callback=None):
        # create a frame which will hold the prompt and user-input space in one line
        frame = Frame(root); frame.pack(anchor = "w")
        # Prompt + Input box, input stored in var
        label = Label(frame, text = label_prompt); label.pack(side=LEFT)
        entry1 = Entry(frame, textvariable = var, width = 10); entry1.pack(side=LEFT, padx=15)
        # calls callback function (if any) after entering input 
        if callback:
            entry1.bind("<Return>", callback) 
        return frame, entry1
    
    
    """
        coordinate_info : Guides the user through a step-by-step process to capture coordinate data
        for etching by interacting with the Signatone device

        Args:
            None
        Returns:
            None
        Raises:
            No errors. Assumes you are connected correctly.
    """
    def coordinate_info():      
        # set flags  
        sig = Signatone()
        chuck_status = False
        caps_status = False
        cap1_status = False
        cap4_status = False

        # list that contains instructions for capturing coordinates, flags for each instruction, variables used for storing for each instructions
        steps = [
                {"label": "  1. Please move stage to the top left corner of the membrane at the top left of grid. (Align the + marker with corner).\n\n  Confirm once the stage is aligned.", "chuck": True, "caps": False, "cap1": False, "cap4": False, "vars": [x_ul_var, y_ul_var]},
                {"label": "  2. Move probes 1 and 4 to touch upper left corner of the grid.\n\n  Confirm once both probes are touching the stage.", "chuck": False, "caps": True, "cap1": True, "cap4": True, "vars": [z_ul_1_var, z_ul_4_var]},
                {"label": "  3. Please move stage to upper right corner of the membrane at the top right of the grid. (Align the + marker with corner).\n\n  Confirm once the stage is aligned.", "chuck": True, "caps": False, "cap1": False, "cap4": False, "vars": [x_ur_var, y_ur_var]},
                {"label": "  4. Move probes 1 and 4 to touch upper right corner of the grid.\n\n  Confirm once both probes are touching the stage.", "chuck": False, "caps": True, "cap1": True, "cap4": True, "vars": [z_ur_1_var, z_ur_4_var]},
                {"label": "  5. Please move stage to lower left corner of the membrane at the bottom left of the grid. (Align the + marker with corner).\n\n  Confirm once the stage is aligned.", "chuck": True, "caps": False, "cap1": False, "cap4": False, "vars": [x_ll_var, y_ll_var]},
                {"label": "  6. Move probes 1 and 4 to touch lower left corner of the grid.\n\n  Confirm once both probes are touching the stage.", "chuck": False, "caps": True, "cap1": True, "cap4": True, "vars": [z_ll_1_var, z_ll_4_var]},
                {"label": "  7. Move stage to the middle of first membrane. (Align the + marker with middle).\n Move probes 1 and 4 slightly above the surface of the grid surrounding the first membrane.\n\n  Lower probes until they touch the sourface. Confirm once ready.", "chuck": False, "caps": True, "cap1": True, "cap4": True, "vars": [z_t_1_var, z_t_4_var]},
                {"label": "  8. Raise the probes back up to no longer touch the surface.\n\n  Confirm once ready.", "chuck": False, "caps": True, "cap1": True, "cap4": True, "vars": [z_e_1_var, z_e_4_var]}
        ]

        current_step = {"index": 0}
        instruction_label = Label(root, text="", wraplength=500, justify=LEFT) # instructions text on gui
        instruction_label.pack(pady=20)
        status_label = Label(root, text="", fg="green") # captured coordinate status on gui
        status_label.pack()
        
        
        """
            capture_coords_for_step : Handles the logic of capturing the coordinate values for the current
            step. Logic includes reading stage or probe positions based on the current step's flags, and storing values. 
            Etch begins after done.

            Args:
                None
            Returns:
                None
            Raises:
                No errors. Assumes you are connected correctly.
            """
        def capture_coords_for_step():
            step = steps[current_step["index"]]
            # Set device flags from step
            chuck_status = step["chuck"]
            caps_status = step["caps"]
            cap1_status = step["cap1"]
            cap4_status = step["cap4"]

            # Capture coordinates based on flags
            if chuck_status and (not caps_status):
                # set device to stage/wafer/chuck, get coordinates of device, store them in corresponding variables
                sig.set_device("WAFER")
                pos_str = sig.get_cap()
                x, y, _ = map(float, pos_str.strip().split(","))
                step["vars"][0].set(f"{x:.1f}")
                step["vars"][1].set(f"{y:.1f}")
                status_label.config(text=f"Captured Stage coords: x={x:.1f}, y={y:.1f}") # print captured coordinates

            elif caps_status and (chuck_status == False):
                # set device to probes/caps, get coordinates of device, store them in corresponding variables
                if cap1_status:
                    sig.set_device("CAP1")
                    pos_str1 = sig.get_cap()
                    z1 = float(pos_str1.strip().split(",")[2])
                    step["vars"][0].set(f"{z1:.1f}")
                if cap4_status:
                    sig.set_device("CAP4")
                    pos_str4 = sig.get_cap()
                    z4 = float(pos_str4.strip().split(",")[2])
                    step["vars"][1].set(f"{z4:.1f}")
                status_label.config(text=f"Captured Probe coords: z1={step['vars'][0].get()}, z4={step['vars'][1].get()}") # print captured coordinates

            # Advance to next instruction
            current_step["index"] += 1
            # if all instructions done, begin the etching process
            if current_step["index"] >= len(steps):
                instruction_label.config(text="All information attained. Ready for etch.\n Click on the membrane center in the image window for calibration.")
                confirm_button.destroy()
                begin_full_etch(int(mem_var.get()), int(row_mem_var.get()), int(street_var.get()), int(grid_len_var.get()), float(x_ul_var.get()), float(y_ul_var.get()), float(z_ul_1_var.get()), float(z_ul_4_var.get()), float(x_ur_var.get()), float(y_ur_var.get()), float(z_ur_1_var.get()), float(z_ur_4_var.get()), float(x_ll_var.get()), float(y_ll_var.get()), float(z_ll_1_var.get()), float(z_ll_4_var.get()), float(z_t_1_var.get()), float(z_t_4_var.get()), float(z_e_1_var.get()), float(z_e_4_var.get()), sig)
            else:
                instruction_label.config(text=steps[current_step["index"]]["label"])

        instruction_label.config(text=steps[0]["label"])
        confirm_button = Button(root, text="Confirm", command=capture_coords_for_step)
        confirm_button.pack(pady=10)


    """
        info_validation : Validates the user's input for etching parameters and proceeds if valid

        Args:
            None
        Returns:
            None
        Raises:
            No errors. Assumes you are connected correctly.
    """
    def info_validation(key):
        # if all inputs are valid, we continue on to get more info (all necessary coordinate values) by calling coordinate_info
        if (mem_var.get().isdigit() & row_mem_var.get().isdigit() & street_var.get().isdigit() & grid_len_var.get().isdigit()):
            for widget in root.winfo_children():
                widget.destroy()
            coordinate_info()
        else:
            lbl = Label(root, text = "One or more of your inputs are invalid. Try again.")
            lbl.pack(anchor = "w")


    """
        grid_info : Handles the user's main menu selection input 

        Args:
            None
        Returns:
            None
        Raises:
            No errors. Assumes you are connected correctly.
    """
    def grid_info(key):  
        user_input = menu_entry.get()
        # Actions depending on if user_input is 1, 2, x, or other
        if user_input == "1":
            # remove what's currently on the page 
            for widget in root.winfo_children():
                widget.destroy()
            # message for user before beginning an etch
            lbl = Label(root, text = "Attention, Attention! Things to note:"); lbl.pack(anchor = "w")
            note1 = Label(root, text = "  1. Be sure that probes are set a safe distance AWAY from the grid to start and voltage is OFF."); note1.pack(anchor = "w")
            note2 = Label(root, text = "  2. Current program runs but at these limitations:\n       - Begins from bottom left and travels in an S-shape.\n       - Probes are aligned with square membrane and a person is taking care of the bubbles.", anchor = "w", justify = "left"); note2.pack(anchor = "w")
            # attain grid information with prompts and input boxes, store inputs in corresponding variables, calls info_validation once all values are entered
            create_labeled_entry(root, "How many membranes are you etching? (enter a number) ", mem_var, callback=info_validation)
            create_labeled_entry(root, "How many membranes are in a row? (enter a number) ", row_mem_var, callback=info_validation)
            create_labeled_entry(root, "What is the width of a street on the membrane? ", street_var, callback=info_validation)
            create_labeled_entry(root, "What is the length of one side of the membrane? ", grid_len_var, callback=info_validation)
        elif user_input == "2":
            root.destroy()
        elif user_input == "x":
            root.destroy()  # Quit the application
        else:
            prompt.configure(text="   Command not valid. Try again.") # If input was not valid
    
    # Main Menu text 
    title = Label(root, text = "Etch Bot Options: "); title.pack(anchor = "w")
    menu_opt_1 = Label(root, text = "   1. Etch a New Grid"); menu_opt_1.pack(anchor = "w")
    menu_opt_2 = Label(root, text = "   2. Reset Devices TBD: Do not use"); menu_opt_2.pack(anchor = "w")
    menu_opt_3 = Label(root, text = "   3. Quit (press x)"); menu_opt_3.pack(anchor = "w")
    # Prompt + Input box
    menu_frame = Frame(root); menu_frame.pack(anchor = "w") # frame which will hold the prompt and user-input box in one line
    prompt = Label(menu_frame, text = "   Enter your choice..."); prompt.pack(side=LEFT)
    menu_entry = Entry(menu_frame, width=10); menu_entry.pack(side=LEFT, padx=15) # User-input box 
    menu_entry.bind("<Return>", grid_info) # Input is used as an argument when calling the grid_info function
    root.mainloop()

if __name__ == "__main__":
    gui_popup()