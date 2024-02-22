import sqlite3
import sys
from pathlib import Path
from os import remove, system
from time import sleep
from difflib import get_close_matches

if getattr(sys, 'frozen', False):
    # if your code is running like exe by Pyinstaller
    ROOT_DIR = Path(sys._MEIPASS)
else:
    # if the code is running inside of IDE
    ROOT_DIR = Path(__file__).parent

ROOT_DIR = Path.home()
app_dir = ROOT_DIR / "Game_library_software"
app_dir.mkdir(exist_ok=True)
DB_FILE = app_dir / "game_db.db"
TABLE_NAME = 'game_library'

# just returns colorful text if you want
def red(text):
    return f'\033[91m{text}\033[0m'
def green(text):
    return f'\033[92m{text}\033[0m'
def blue(text):
    return f'\033[94m{text}\033[0m'
def yellow(text):
    return f'\033[93m{text}\033[0m'

def create_db():
    # create db if not exists
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    cursor.execute(
        f'CREATE TABLE IF NOT EXISTS {TABLE_NAME}'
        '('
        'id INTEGER PRIMARY KEY AUTOINCREMENT,'
        'name TEXT INTEGER NOT NULL,'
        'category TEXT INTEGER NOT NULL,'
        'plataform TEXT INTEGER NULL'
        ")"
    )
    cursor.close()
    connection.close()
    
def create_game_dict() -> str:
    """
    Creates a dictionary with user input for a new game.

    Returns:
    dict: A dictionary containing game information.
    """
    game = {}
    validate_answer = False

    while not validate_answer:
        game['name'] = str(input('Game name: ')).capitalize().strip()
        if not game['name']:
            print('Please, you need to write one game at least.')
            print()
            sleep(0.5)
        else:
            validate_answer = True
        validate_answer = False
        
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute(
            f'SELECT "name" FROM {TABLE_NAME} WHERE "name" LIKE ?', (game['name'],)    
        )
        result = cursor.fetchone()
        
        if result:
            print('the game that you write already exists in your library.')
            print()
            sleep(0.5)
        else:
            validate_answer = True
            
    validate_answer = False # You must put the 'validate_answer' to False after this while, because the code is gonna break without this.
    while not validate_answer:
        game['category'] = str(input('Category: ')).capitalize().strip()
        if not game['category']:
            print('Please, you need to write one category at least.')
            print()
            sleep(0.5)
        else:
            validate_answer = True
    
    validate_answer = False # You must put the 'validate_answer' to False after this while, because the code is gonna break without this.
    
    while not validate_answer:
        exclusive = str(input('This game is exclusive for any plataform?(YES or NO) ->  ')).upper().strip()
        if not exclusive:
            print('Please, just answer with YES or NO.')
            print()
            sleep(0.5)
            
        elif exclusive not in ('YES', 'NO'):
            print('Please, just answer with YES or NO.')
            print()
            sleep(0.5)
        else:
            validate_answer = True
        print()
            
    validate_answer = False # You must put the 'validate_answer' to False after this while, because the code is gonna break without this.
    
    while not validate_answer:
        if exclusive =='YES':
            consoles = ['Playstation', 'Xbox', 'Nintendo', 'Pc']
            print('-Just Playstation, Xbox, Nintendo and Pc are aceppted-')
            game['plataform'] = str(input('Plataform ->')).capitalize()
            print()
            if game['plataform'] in consoles:        
                validate_answer = True
                
            elif not game['plataform']:
                print('- Something is wrong :( -')
                print()
                sleep(0.5)
                
            else:
                near_console = get_close_matches(game['plataform'], consoles, n=1, cutoff=0.5) # fuction to search similar words in consoles list
                if near_console:
                    print(f'Did you mean to say "{near_console[0]}"?')
                    print()
                else:
                    print('- Something is wrong :( -')
                    print()
                    sleep(0.5)

        # I put the db to consider plataform to null, because it expect one value, if you select 'NO' above, column plataform becomes optional.
        elif exclusive == 'NO':
            game['plataform'] = None
            validate_answer = True
    return game

def add_on_db() -> str:
    dicionary = create_game_dict()
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    cursor.execute(
        f'INSERT INTO {TABLE_NAME} '
        '(id, name, category, plataform) '
        'VALUES '
        f'(NULL, :name, :category, :plataform)', dicionary
    )
    connection.commit()
    
    print('Your game is saved on Library!')
    sleep(3)
    system('cls')

    cursor.close()
    connection.close()

def select_by(selected, value):
    """
    Selects games from the database based on a specific criterion.

    Args:
    selected (str): The criterion for selection (e.g., 'name', 'category').
    value (str): The value to match in the selected criterion.

    Returns:
    str: Formatted string with information about selected games.
    """
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    
    cursor.execute(
        f'SELECT "name", "category", "plataform" FROM {TABLE_NAME} WHERE "{selected}" LIKE ?', (value + '%',)
    )
    result = cursor.fetchall()
    
    if result:
        output = ""
        
        for row in result:
            name, category, plataform = row
            if plataform is not None:
                if plataform == 'Playstation':
                    output += blue(f'''
----------------------------------------
    Game name: {name}
    Category: {category}
    Exclusive: {plataform}
----------------------------------------
                ''')
                if plataform == 'Xbox':
                    output += green(f'''
----------------------------------------
    Game name: {name}
    Category: {category}
    Exclusive: {plataform}
----------------------------------------
                ''')
                if plataform == 'Nintendo':
                    output += red(f'''
----------------------------------------
    Game name: {name}
    Category: {category}
    Exclusive: {plataform}
----------------------------------------
                ''') 
                if plataform == 'Pc':
                    output += yellow(f'''
----------------------------------------
    Game name: {name}
    Category: {category}
    Exclusive: {plataform}
----------------------------------------
                ''')
            else:
                output += f'''
----------------------------------------
    Game name: {name}
    Category: {category}
----------------------------------------
            '''
        cursor.close()
        connection.close()
        
        return print(f'''I found this games...
                {output}''')
    else:
        print("I didn't find any value with this word.")
        print()

def select_name_from_db(name) -> str:
   select_by('name', name)
        
def delete_all_db(): 
    """
    Deletes all games from the database, including the file.
    To create the file again, call 'create_db' and the file is gonna be created.

    Returns:
    None
    """
    print('Warning, all data is gonna deleted')
    sleep(1)
    while True:
        final_option = str(input('You really wanna delete entire db?[Yes/No] ')).upper()
        if final_option == 'YES':
            remove(DB_FILE)
            print()
            print('All db has been deleted!')
            print('To create a new BD, rerun the software.')
            sleep(3)
            exit()
            
        elif final_option == 'NO':
            print()
            print('Ok, your data is not deleted!:), lets continue')
            sleep(3)
            system('cls')
            break
        print()
        print('Please, just answer with YES or NO.')

def show_all_games():
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    
    cursor.execute(
        f'SELECT "name", "category", "plataform" FROM {TABLE_NAME}'
    )
    result = cursor.fetchall()
    
    output = ""
    
    for row in result:
        name, category, plataform = row
        if plataform is not None:
            if plataform == 'Playstation':
                output += blue(f'''
----------------------------------------
    Game name: {name}
    Category: {category}
    Exclusive: {plataform}
----------------------------------------
        ''')
            if plataform == 'Xbox':
                output += green(f'''
----------------------------------------
    Game name: {name}
    Category: {category}
    Exclusive: {plataform}
----------------------------------------
        ''')
            if plataform == 'Nintendo':
                output += red(f'''
----------------------------------------
    Game name: {name}
    Category: {category}
    Exclusive: {plataform}
----------------------------------------
        ''') 
            if plataform == 'Pc':
                output += yellow(f'''
----------------------------------------
    Game name: {name}
    Category: {category}
    Exclusive: {plataform}
----------------------------------------
        ''')
        else:
            output += f'''
----------------------------------------
    Game name: {name}
    Category: {category}
----------------------------------------
    '''
            
    cursor.close()
    connection.close()
    
    return f'''Thats all folks!!!  :)
            {output}'''

def select_category(name_) -> str:
    select_by('category', name_)

def select_plataform(name_) -> str:
    select_by('plataform', name_)
           
def delete_from_db(game_to_delete) -> str:
    """
    Deletes a specific game from the database.

    Args:
    game_to_delete (str): The name of the game to delete.

    Returns:
    None
    """
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    
    cursor.execute(
        f'SELECT "name", "category", "plataform" FROM {TABLE_NAME} WHERE "name" = ?', (game_to_delete,)
    )
    result = cursor.fetchall()
    
    if result:
        output = ""
        
        for row in result:
            name, category, plataform = row
            if plataform is not None:
                output += f'''
----------------------------------------
    Game name: {name}
    Category: {category}
    Exclusive: {plataform}
----------------------------------------
            '''
            else:
                output += f'''
----------------------------------------
    Game name: {name}
    Category: {category}
----------------------------------------
            '''
            
        while True:
            print()
            print(f'You really wish to delete this record?')
            print(f'{output}')
            choice = str(input('Yes or No: ')).upper()
            if choice == 'YES':
                cursor.execute(
                    f'DELETE FROM {TABLE_NAME} WHERE name = ?', (game_to_delete,)
                )
                connection.commit()
                print()
                print('Ok, this line in you bd is deleted sucessfully :)!')
                input('Press Enter key to continue!')
                sleep(2)
                system('cls')
                break
            
            elif choice == 'NO':
                print()
                print('Ok, i not delete this!')
                input('Press Enter key to continue!')
                sleep(2)
                system('cls')
                break
            print('Please, just choice between yes or no.')
            
        cursor.close()
        connection.close()
    else:
        print("I didn't find any game with this word, please try again.")
        print()
        input('Press Enter key to continue!')
        sleep(1)
        system('cls')
        
def menu():
    welcome = '''
Welcome to your personal game database
This storage software was made to you dont forget your favorite games!
    '''
    print(welcome)   
     
    menu = '''
    [1] Add game
    [2] Delete all games
    [3] Delete specify game
    [4] Search for game(s)
    [5] Search for categories
    [6] Search for plataform(s)
    [7] Show all games
    [8] Close software
    '''
    print(menu)
    while True:
        choice = str(input('What you will do -> ')).strip()
        if not choice: 
            print('Please, select JUST numbers in menu.')
            print()
            input('Press Enter to retry!')
            sleep(1)
            system('cls')    
            
        if choice in '12345678':
            return choice

        else: 
            print('Please, select JUST numbers in menu.')
            print()
            input('Press Enter to retry!')
            sleep(1)
            system('cls')
            print(welcome)
            print(menu)
 
if __name__ == '__main__' :
    pass
