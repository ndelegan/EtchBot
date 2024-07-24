"""

    Menu options to simulate a automated machine during testing.

    Authors: UIC Chicago Tech Circle Team (Lisset Rico, Fernanda Villalpando)
    Collaborator(s): Argonne National Laboratory (Nazar Delegan, Clayton Devault)
    Date Created: 06/26/2024

"""

import etching as Etching
# import water_pump as Water

opt = ''

print('Welcome to Etch Bot!')

# while loop for menu options
while opt != 'x':
    print('Etch Bot Options: ')
    print('   1. Etch a Grid')
    print('   2. Reset Devices')
    print('   3. Quit (press x)')
    
    opt = input('Select an Option (Enter the number of the option): ')
    if opt == '1':
        print('Attention, Attention!')
        print('***Be sure that probes are set a safe distance away to start and voltage is off.')
        print('***Current program only etches one square assuming: probes are aligned with square membrane and a person is taking care of the bubbles.')
        print('***For rows and cols inputs only enter 1.')
        
        # etch one square, assuming device setup correctly
        # etch one square but probes aren't aligned
        
        # etch full grid, not ready yet
        row = input("How many rows are in the grid? ")
        col = input("How many cols are in the grid? ")
        Etching.full_grid_etch(row, col)
    elif opt == '2':
        print('resetting')
    elif opt == 'x':
        # quit and move devices once done aka reset everything for the day
        quit()
    else:
        print("Command not valid. Try again.")
        
print('Have a good day! :)')
quit()