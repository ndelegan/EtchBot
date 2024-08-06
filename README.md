# EtchBot
Common repository for code and documentation of the 2024 BTTC Summer Project in the Argonne Foundry related to autonomous etching of membranes.

Chicago Tech Circle and Argonne

Author(s): Fernanda Villalpando, Lisset Rico,Claudia Jimenez, Aima Qutbuddin, Lisette Ruano, Andrea Muñoz

Argonne Collaborator(s): Nazar Delegan, Clayton Devault

Break Through Tech Collaborator(s): Kyle Cheek

Overview:

* Our task is to automate the etching process of diamond membranes using a computer vision, Signatone Voltage Source and Signatone Station Controls. 

Current Progress (08/08):
 - GitHub localization
 - Sending a slack message from bubbles and tether detection
 - Signatone and Siglent Device Drivers
 - Pre-Etch: Detects the square
 - Can detect unetched area when image is cropped for a single square (about 97% when starting and 7% when done)
 - Runable etching program (For 1 membrane) In-person or remote
 - Traversal through the entire grid using GDS coordinates
 - Water Pump by itself works
 - Program has menu options like a automated machine would

To-Do (08/08):
 - Refine existing code
 - Convert pixel to device coordinates
 - Use robust and formal testing
