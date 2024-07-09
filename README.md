# EtchBot
Common repository for code and documentation of the 2024 BTTC Summer Project in the Argonne Foundry related to autonomous etching of membranes.

Chicago Tech Circle and Argonne

Author(s): Fernanda Villalpando, Lisset Rico,Claudia Jimenez, Aima Qutbuddin, Lisette Ruano, Andrea Muñoz

Argonne Collaborator(s): Nazar Delegan, Clayton Devault

Break Through Tech Collaborator(s): Kyle Cheek

Overview:

* Our task is to automate the etching process of diamond membranes using a Signatone Voltage Source, Signatone Probe Controls. 

Current Progress Made:

 - Bubble Bot (Recognition + Sending a Slack Message)
 - Tether Bot (Recognition + Sending a Slack Message)
 - Signatone and Siglent Device Driver
 - Pre-Etch: Detects the square
 - Post Etch: Can detect leftover area when image is cropped for a single square (about 7% dark area left)
 - Github localization
 - Etching File combining all bots and functions is made
 - Water Pump by itself works

Images:

To-Do
 - Refine existing code
 - Use GDS files to pull measurements
 - Convert pixel to device coordinates
 - Start moving from initial membrane to another
 - Use robust and formal testing
 - Menu options
 - Remotely Etching
