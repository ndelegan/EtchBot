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
    print('Pick an Option: ')
    if opt == '1':
        # etch full grid, not ready yet
            # tell me your grid size
        # Etching.full_grid()
        pass
    elif opt == '2':
        # etch one square but probes aren't aligned
        # Etching.square_vtwo()
        pass
    elif opt == '3':
        # etch one square, assuming device setup correctly
        row = input("What is the row count?")
        col = input("What is the col count?")
        Etching.cut(row, col)
    elif opt == 'x':
        # quit and move devices once done aka reset everything for the day
        quit()
    else:
        print("Command not valid. Try again.")
        
print('Have a good day! :)')