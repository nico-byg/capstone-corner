''' main.py - the point of entry for the application. Provides 
system administrators with a command line based interface to interact with the application.
Author: Nick Colby
'''

from cli_methods import print_menu, setup_migration, make_migration

def main():
    print("Welcome to the CSV Reader Application!")
    
    run = True
    while run:
        print_menu()

        # Get user input for the menu choice
        choice = input("\nEnter your selection: ")
        
        if choice == '1':
            setup_migration()
        
        elif choice == '2':
            make_migration()
        
        elif choice == '3':
            run = False
            print("Exiting the application. Goodbye!")
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
