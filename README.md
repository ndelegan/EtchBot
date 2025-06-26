# EtchBot
Common repository for code and documentation of the 2024/2025 BTTC Chicago Tech Circle Summer Project in the Argonne Foundry related to autonomous etching of membranes.

Author(s): 2024 cohort: Fernanda Villalpando, Lisset Rico, Claudia Jimenez, Aima Qutbuddin, Lisette Ruano, Andrea Muñoz
           2025 cohort: Yana Ninovska, Michelle Montesinos, Elizabeth Ng, Daisy Maldonado

Argonne Collaborator(s): Nazar Delegan, Clayton Devault

Break Through Tech Collaborator(s): Kyle Cheek

## Overview:

* Our task is to automate the etching process of diamond membranes using a computer vision, Signatone Voltage Source and Signatone Station Controls. 


## Current Progress (06/26/25):
 - Created a GUI for Siglent with interactive controls.
 - Built a main GUI to improve user experience and system control.
 - Automated probe lowering using a tilt-based algorithm.
 - Switched to Affine Calibration for more accurate square positioning.
 - Improved etch detection by switching from grayscale to color-based analysis.
 - Used water pump code, but currently facing hardware issues. 
 - Removed bubble detection and now activate the water pump each time a picture is taken.

## Past Progress (08/08/24):
 - GitHub localization.
 - Sending a slack message from bubbles and tether detection.
 - Signatone and Siglent Device Drivers using Python.
 - Pre-Etch: Detects the square.
 - Can detect unetched area when image is cropped for a single square (about 97% when starting and 7% when done).
 - Runable etching program (For 1 membrane) In-person or remote.
 - Traversal through the entire grid using GDS coordinates.
 - Water Pump by itself works.
 - Program has menu options.


## Running the Program
There are one way to run this program.


###  Using the GUI to populate grid parameters
1. Run the etching_gui.py file by using the command 
   ``` python etching_gui.py ```.
2. Once you start the program you will be asked questions to fill the parameters used in the full_grid_etch function in etching_main.py.