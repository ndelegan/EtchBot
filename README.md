# EtchBot
Common repository for code and documentation of the 2024 BTTC Summer Project in the Argonne Foundry related to autonomous etching of membranes.

Chicago Tech Circle and Argonne

Author(s): Fernanda Villalpando, Lisset Rico, reporting on additional work done by Claudia Jimenez, Aima Qutbuddin, Lisette Ruano, Andrea Muñoz
Argonne Collaborator(s): Nazar Delegan, Clayton Devault

Overview:

Our task is to automate the etching process of diamond membranes using a Signatone Voltage Source, Signatone Probe Controls. 

Current Progress Made:

Bubble Bot (Recognition + Sending a Slack Message)
Tether Bot (Recognition + Sending a Slack Message)
Signatone and Siglent Device Driver
Diamond Square Recognition
Pre-Etch: Partially detects squares not all in an image
Post Etch: Can detect leftover area when image is cropped for a single square (about 7% dark area left at the moment)

Images:

To-Do
 - Combine separate coding segments into concise python file called etching automation
 - Create documentation for etching automation file, pyvisa x scpi commands.
 - Motor Pump
 - Set up Github Repo
 - Download VSCode, Git, Github Desktop onto remote desktop, CV2 (use this line of code → pip install opencv-contrib-python)
 - Refine already existing code
