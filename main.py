"""

    Menu options to simulate an automated machine during testing.

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
    print('   1. Etch a New Grid')
    print('   2. Reset Devices')
    print('   3. Quit (press x)')
    
    opt = input('Select an Option (Enter the number of the option): ')
    if opt == '1':
        print('Attention, Attention!')
        print('  1. Be sure that probes are set a safe distance up from the grid to start and voltage is off.')
        print('  2. Current program runs at these limitations:')
        print('     Begins from bottom left and travels in an S-shape.')
        print('     Probes are aligned with square membrane and a person is taking care of the bubbles.')
        print('  3. Testing with only 1 membrane.')
        
        # etch one square, assuming device setup correctly; probe movement still in process
        membranes = input("How many membranes are in the grid? ")
        Etching.full_grid_etch(membranes)
    elif opt == '2':
        print('resetting')
    elif opt == 'x':
        # quit and move devices once done aka reset everything for the day
        quit()
    else:
        print("Command not valid. Try again.")
        
print('Have a good day! :)')
quit()