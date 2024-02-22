from manipulate_db import *
from time import sleep

create_db()
running = True

while running:
    choice = menu()
    if choice == '1':
        add_on_db()
            
    elif choice == '2':
        print()
        delete_all_db()
            
    elif choice == '3':
        print()
        game_to_delete = str(input('Game to delete -> ')).capitalize().strip()
        delete_from_db(game_to_delete)

    elif choice == '4':
        validate = False   
        while not validate:
            game_to_search = str(input('Game to search -> ')).capitalize().strip()
            if not game_to_search:
                print('Write one game at least.')
                print()
            else:
                validate = True
        print()
        select_name_from_db(game_to_search)
        input('Press Enter key to continue!')
        sleep(2)
        system('cls')
        
    elif choice == '5':
        validate = False   
        while not validate:
            category_to_search = str(input('Category to search -> ')).capitalize().strip()
            if not category_to_search:
                print('Write one category at least.')
                print()
            else:
                validate = True
        print()
        select_category(category_to_search)
        input('Press Enter key to continue!')
        sleep(2)
        system('cls')
    
    elif choice == '6':
        validate = False
        while not validate:
            print('Remember, Just Playstation, Xbox, Nintendo and Pc are aceppted.')
            plataform_to_search = str(input('Plataform to search -> ')).capitalize().strip()
            if not plataform_to_search:
                print('Write one Plataform at least')
                print()
            else:
                validate = True
        print()
        select_plataform(plataform_to_search)
        input('Press Enter key to continue!')
        sleep(2)
        system('cls')
    
    elif choice == '7':
        sleep(2)
        system('cls')
        print('Ok, i will show all games in your library!')
        sleep(2)
        print(show_all_games())
        input('Press Enter key to return to menu!')
        system('cls')
    
    elif choice == '8':
        print('Ok, see you later! :)')
        sleep(1)
        running = False
        