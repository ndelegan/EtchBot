"""

    Menu options for etching.

    Authors: UIC Chicago Tech Circle Team (Lisset Rico, Fernanda Villalpando)
    Collaborator(s): Argonne National Laboratory (Nazar Delegan, Clayton Devault)
    Date Created: 06/26/2024

"""

import etching as Etching
import water_pump as Water

opt = ''

# menu options

print('Welcome to Etch Bot!')

Water.turn_on()

while opt != 'x':
    print('Select an Option (Enter the number of the option): ')
    if opt == '1. Etch a Grid':
        # etch full grid, not ready yet
        # etch one square but probes aren't aligned
        # etch one square, assuming device setup correctly
        row = input("How many rows are in the grid?")
        col = input("How many cols are in the grid?")
        Etching.cut(row, col)
    elif opt == 'x':
        # quit and move devices once done aka reset everything for the day
        quit()
    else:
        print("Command not valid. Try again.")
        
print('Have a good day! :)')
quit()