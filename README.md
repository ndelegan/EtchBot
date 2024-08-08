# EtchBot
Common repository for code and documentation of the 2024 BTTC Chicago Tech Circle Summer Project in the Argonne Foundry related to autonomous etching of membranes.

Author(s): Fernanda Villalpando, Lisset Rico, Claudia Jimenez, Aima Qutbuddin, Lisette Ruano, Andrea Muñoz

Argonne Collaborator(s): Nazar Delegan, Clayton Devault

Break Through Tech Collaborator(s): Kyle Cheek

## Overview:

* Our task is to automate the etching process of diamond membranes using a computer vision, Signatone Voltage Source and Signatone Station Controls. 

## Current Progress (08/08):
 - GitHub localization
 - Sending a slack message from bubbles and tether detection
 - Signatone and Siglent Device Drivers using Python
 - Pre-Etch: Detects the square
 - Can detect unetched area when image is cropped for a single square (about 97% when starting and 7% when done)
 - Runable etching program (For 1 membrane) In-person or remote
 - Traversal through the entire grid using GDS coordinates
 - Water Pump by itself works
 - Program has menu options

## To-Do (08/08):
 - Make GitHub private
 - Refine existing code
 - Convert pixel to device coordinates for probe movement through machine learning
 - Use robust and formal testing

## Running the Program
There are two ways to run this program.

### First Option: Manually entering grid parameters into the code
1. Open the etching.py file and scroll to the bottom of the page
2. You will see a call for the function called full_grid_etch with all the parameters that are passed into the function
3. If the chuck has moved from last time or unsure if it's where it was left last time update these parameters as neccessary.
4. Run the file by using the command ```python etching.py```

### Second Option: Using the menu option to populate grid parameters
1. Run the main.py file by using the command ``` python main.py ```
2. Once you start the program you will be asked questions to fill the parameters used in the full_grid_etch function in etching.py.