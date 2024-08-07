"""

    Menu options to simulate an automated machine during testing.

    Authors: UIC Chicago Tech Circle Team (Lisset Rico, Fernanda Villalpando)
    Collaborator(s): Argonne National Laboratory (Nazar Delegan, Clayton Devault)
    Date Created: 06/26/2024

"""

import etching as Etching

def main():
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
            print('Attention, Attention! Things to note:')
            print('  1. Be sure that probes are set a safe distance AWAY from the grid to start and voltage is OFF.')
            print('  2. Current program runs but at these limitations:')
            print('     Begins from bottom left and travels in an S-shape.')
            print('     Probes are aligned with square membrane and a person is taking care of the bubbles.')
            print('     Asks for  user confirmation to move from one membrane to the next.')
            print('  3. Full etching testing has only been conducted with 1 membrane.')
            
            # get stats: # of membranes, # of membranes in row, street length, grid length, lower-left, upper-left, upper-right corner grid coordinates
            mem = input('How many membranes are you etching(enter a number)? ')
            row_mem = input('How many membranes are in a row(enter a number)? ')
            street = input("What is the width of a street on the membrane? ")
            grid_len = input("What is the length of one side of the membrane? ")
            x_ll, y_ll = input('What is the lower-left grid corner coordinates(enter \'x y\' rounded up)? ').split()
            x_ul, y_ul = input('What is the upper-left grid corner coordinates(enter ''x y'' rounded up)? ').split()
            x_ur, y_ur = input('What is the upper-right grid corner coordinates(enter ''x y'' rounded up)? ').split()
            
            Etching.full_grid_etch(int(mem), int(row_mem), int(street), int(grid_len), int(x_ll), int(y_ll), int(x_ul), int(y_ul), int(x_ur), int(y_ur))
        elif opt == '2':
            print('resetting')
        elif opt == 'x':
            quit()
        else:
            print('Command not valid. Try again.')
            
    print('Have a good day! :)')
    quit()

if __name__ == '__main__':
    main()