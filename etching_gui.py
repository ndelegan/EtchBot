"""
    GUI that allows the use of etching

    Authors: UIC Chicago Tech Circle Team (Daisy Maldonado)
    Collaborators: Argonne National Laboratory (Nazar Delegan, Clayton Devault)
    Date Created: 06/23/2025
"""

from tkinter import *
import etching as Etching
import tkinter as tk
from signatone_driver import Signatone
from siglent_gui import gui_popup as launch_siglent_gui
import threading
from etching_main import full_grid_etch as begin_full_etch


# def open_siglent_gui(parent):
#     window = tk.Toplevel(parent)
#     window.title("Siglent Control")
#     # build your siglent GUI here inside `window`
#     tk.Label(window, text="Siglent GUI").pack()

def start_siglent():
    threading.Thread(target=launch_siglent_gui).start()
    
def gui_popup():
    # root window
    root = Tk()
    root.title("Welcome to Etch Bot!")
    root.geometry('600x350')
    start_siglent()
    # Variables which will assist in the arguments for Etching.full_grid_etch
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

    def create_labeled_entry(root, label_prompt, var, var2=None, callback=None):
        # create a frame which will hold the prompt and user-input space in one line
        frame = Frame(root)
        frame.pack(anchor = "w")

        # display the prompt
        label = Label(frame, text = label_prompt)
        label.pack(side=LEFT)

        # allow user input 
        entry1 = Entry(frame, textvariable=var, width=10)
        entry1.pack(side=LEFT, padx=15)

        if callback:
            #entry1.bind("<Return>", lambda event: callback(var.get()))
            entry1.bind("<Return>", callback)
        
        if var2:
            entry2 = Entry(frame, textvariable=var2, width=10)
            entry2.pack(side=LEFT, padx=15)
            if callback:
                #entry2.bind("<Return>", lambda event: callback(var2.get()))
                entry2.bind("<Return>", callback)
            return frame, entry1, entry2    
        return frame, entry1
    
    
    def coord():        
        sig = Signatone()
        chuck_status = False
        caps_status = False
        cap1_status = False
        cap4_status = False

        steps = [
                {"label": "  1. Please move stage to upper left corner of the grid. (Align the + marker with corner).\n\n  Confirm once the stage is aligned.", "chuck": True, "caps": False, "cap1": False, "cap4": False, "vars": [x_ul_var, y_ul_var]},
                {"label": "  2. Move probes 1 and 4 to touch upper left corner of the grid.\n\n  Confirm once both probes are touching the stage.", "chuck": False, "caps": True, "cap1": True, "cap4": True, "vars": [z_ul_1_var, z_ul_4_var]},
                {"label": "  3. Please move stage to upper right corner of the grid. (Align the + marker with corner).\n\n  Confirm once the stage is aligned.", "chuck": True, "caps": False, "cap1": False, "cap4": False, "vars": [x_ur_var, y_ur_var]},
                {"label": "  4. Move probes 1 and 4 to touch upper right corner of the grid.\n\n  Confirm once both probes are touching the stage.", "chuck": False, "caps": True, "cap1": True, "cap4": True, "vars": [z_ur_1_var, z_ur_4_var]},
                {"label": "  5. Please move stage to lower left corner of the grid. (Align the + marker with corner).\n\n  Confirm once the stage is aligned.", "chuck": True, "caps": False, "cap1": False, "cap4": False, "vars": [x_ll_var, y_ll_var]},
                {"label": "  6. Move probes 1 and 4 to touch lower left corner of the grid.\n\n  Confirm once both probes are touching the stage.", "chuck": False, "caps": True, "cap1": True, "cap4": True, "vars": [z_ll_1_var, z_ll_4_var]},
                {"label": "  7. Move probes 1 and 4 slightly above the surface of the grid surrounding the first membrane.\n\n  Lower probes until they touch the sourface. Confirm once ready.", "chuck": False, "caps": True, "cap1": True, "cap4": True, "vars": [z_t_1_var, z_t_4_var]},
                {"label": "  8. Raise the probes back up to no longer touch the surface.\n\n  Confirm once ready.", "chuck": False, "caps": True, "cap1": True, "cap4": True, "vars": [z_e_1_var, z_e_4_var]}
        ]

        current_step = {"index": 0}

        instruction_label = Label(root, text="", wraplength=500, justify=LEFT)
        instruction_label.pack(pady=20)

        status_label = Label(root, text="", fg="green")
        status_label.pack()
        
        def capture_coords_for_step():
           
            step = steps[current_step["index"]]

            # Set device flags from step
            chuck_status = step["chuck"]
            caps_status = step["caps"]
            cap1_status = step["cap1"]
            cap4_status = step["cap4"]
            print("drn:", chuck_status)
            print("prn:", caps_status )

            # Capture coordinates based on flags
            if chuck_status and (not caps_status):
                sig.set_device("WAFER")
                dev = sig.get_device()
                print(dev)
                pos_str = sig.get_cap()
                x, y, _ = map(float, pos_str.strip().split(","))
                step["vars"][0].set(f"{x:.1f}")
                step["vars"][1].set(f"{y:.1f}")
                status_label.config(text=f"Captured Stage coords: x={x:.1f}, y={y:.1f}")

            elif caps_status and (chuck_status == False):
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
                status_label.config(text=f"Captured Probe coords: z1={step['vars'][0].get()}, z4={step['vars'][1].get()}")

            # Advance step
            current_step["index"] += 1
            if current_step["index"] >= len(steps):
               
                instruction_label.config(text="All information attained. Ready for etch.")
                # confirm_button.config(state=DISABLED)
                confirm_button.destroy()
                # print(mem_var.get(), row_mem_var.get(), street_var.get(), grid_len_var.get(), x_ul_var.get(), y_ul_var.get(), z_ul_1_var.get(), z_ul_4_var.get(), x_ur_var.get(), y_ur_var.get(), z_ur_1_var.get(), z_ur_4_var.get(), x_ll_var.get(), y_ll_var.get(), z_ll_1_var.get(), z_ll_4_var.get(), z_t_1_var.get(), z_t_4_var.get(), z_e_1_var.get(), z_e_4_var.get())
                #full_grid_etch(3, 9, 75, 250, -18240, -6840, -18157, -9667, -20981, -9744)
                # begin_full_etch(int(mem_var.get()), int(row_mem_var.get()), int(street_var.get()), int(grid_len_var.get()), float(x_ul_var.get()), float(y_ul_var.get()), float(z_ul_1_var.get()), float(z_ul_4_var.get()), float(x_ur_var.get()), float(y_ur_var.get()), float(z_ur_1_var.get()), float(z_ur_4_var.get()), float(x_ll_var.get()), float(y_ll_var.get()), float(z_ll_1_var.get()), float(z_ll_4_var.get()), float(z_t_1_var.get()), float(z_t_4_var.get()), float(z_e_1_var.get()), float(z_e_4_var.get()))
                begin_full_etch(3,9,75,250, -17425.3, -12594.3, -5525.8, -9170.6, -20251.5, -12641.3, -5468.2, -9124.2, -17480.2, -9765.2, -5473.4, -9129.5, -5473.7, -9142, -5374.3, -8987)
                # print("Captured variables:")
                # for s in steps:
                #     print(s["label"], [v.get() for v in s["vars"]])
            else:
                instruction_label.config(text=steps[current_step["index"]]["label"])

        instruction_label.config(text=steps[0]["label"])

        confirm_button = Button(root, text="Confirm", command=capture_coords_for_step)
        confirm_button.pack(pady=10)


    def info_input(key):
        # if all inputs are valid, they are stored in corresponding variables
        if (mem_var.get().isdigit() & row_mem_var.get().isdigit() & street_var.get().isdigit() & grid_len_var.get().isdigit() ):
            # & x_ll_var.get().isdigit & y_ll_var.get().isdigit() & x_ul_var.get().isdigit & y_ul_var.get().isdigit() & x_ur_var.get().isdigit() & y_ur_var.get().isdigit()
            mem = mem_var.get()
            row_mem = row_mem_var.get()
            street = street_var.get()
            grid_len = grid_len_var.get()
       

            for widget in root.winfo_children():
                widget.destroy()

            print(mem, row_mem, street, grid_len)
            # begin etch 
            # Etching.full_grid_etch(int(mem), int(row_mem), int(street), int(grid_len), int(x_ll), int(y_ll), int(x_ul), int(y_ul), int(x_ur), int(y_ur))
    
            # coords_instructions(0)
            coord()


        else:
            print("One or more of your inputs are invalid. Try again.")
            lbl = Label(root, text = "One or more of your inputs are invalid. Try again.")
            lbl.pack(anchor = "w")


    def menu_input(key):  
        user_input = menu_entry.get()
        if user_input == "1":
            # remove what's currently on the page 
            for widget in root.winfo_children():
                widget.destroy()

            # message for user before beginning an etch
            lbl = Label(root, text = "Attention, Attention! Things to note:")
            lbl.pack(anchor = "w")
            note1 = Label(root, text = "  1. Be sure that probes are set a safe distance AWAY from the grid to start and voltage is OFF.")
            note1.pack(anchor = "w")
            note2 = Label(root, text = "  2. Current program runs but at these limitations:\n       - Begins from bottom left and travels in an S-shape.\n       - Probes are aligned with square membrane and a person is taking care of the bubbles.\n       - Asks for  user confirmation to move from one membrane to the next.", anchor = "w", justify = "left")
            note2.pack(anchor = "w")
            note3 = Label(root, text = "  3. Full etching testing has only been conducted with 1 membrane.\n")
            note3.pack(anchor = "w")

            # Prompts user for input. # of membranes, size of membrane, and coordinates are asked for

            # info_frame = Frame(root)
            # info_frame.pack(anchor = "w")

            # start5 = Label(info_frame, text = "How many membranes are you etching? (enter a number) ")
            # start5.pack(side=LEFT)

            # s6 = Entry(info_frame, textvariable=mem_var, width=10)
            # s6.pack(side=LEFT, padx=15) 
            # s6.bind("<Return>", info_input) 
            create_labeled_entry(root, "How many membranes are you etching? (enter a number) ", mem_var, callback=info_input)

            create_labeled_entry(root, "How many membranes are in a row? (enter a number) ", row_mem_var, callback=info_input)

            create_labeled_entry(root, "What is the width of a street on the membrane? ", street_var, callback=info_input)

            create_labeled_entry(root, "What is the length of one side of the membrane? ", grid_len_var, callback=info_input)
            

            # create_labeled_entry(root, "What is the lower-left grid corner coordinates? (enter \'x y\' rounded up) ", x_ll_var, y_ll_var, info_input)
            # create_labeled_entry(root, "What is the upper-left grid corner coordinates? (enter ''x y'' rounded up) ", x_ul_var, y_ul_var, info_input)
            # create_labeled_entry(root, "What is the upper-right grid corner coordinates? (enter ''x y'' rounded up) ", x_ur_var, y_ur_var, info_input)

        elif user_input == "2":
            # for widget in root.winfo_children():
            #     widget.destroy()

            root.destroy()

        elif user_input == "x":
            root.destroy()  # Quit the application
        else:
            lbl5.configure(text="   Command not valid. Try again.") # If input was not valid
    

    # Main Menu 
    title = Label(root, text = "Etch Bot Options: ")
    title.pack(anchor = "w")
    menu_opt_1 = Label(root, text = "   1. Etch a New Grid")
    menu_opt_1.pack(anchor = "w")
    menu_opt_2 = Label(root, text = "   2. Reset Devices TBD: Do not use")
    menu_opt_2.pack(anchor = "w")
    menu_opt_3 = Label(root, text = "   3. Quit (press x)")
    menu_opt_3.pack(anchor = "w")

    # create a frame which will hold the prompt and user-input space in one line
    menu_frame = Frame(root)
    menu_frame.pack(anchor = "w")

    lbl5 = Label(menu_frame, text = "   Enter your choice...")
    lbl5.pack(side=LEFT)

    # Use input as the argument for menu_input
    menu_entry = Entry(menu_frame, width=10)
    menu_entry.pack(side=LEFT, padx=15) 
    menu_entry.bind("<Return>", menu_input)  
    # create_labeled_entry(menu_frame, "   Enter your choice...", StringVar(), menu_input)
    root.mainloop()


if __name__ == "__main__":
    gui_popup()