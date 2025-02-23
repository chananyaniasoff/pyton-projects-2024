import random
import time
from PIL import Image, ImageT
import tkinter as tk
from tkinter import messagebox

GAME_LIST = ['rock', 'paper', 'scissors']
USR_POINTS = 0
PLAYER2_POINTS = 0
COMUTER_POINTS = 0
GAMES_PLAYED = 0
NEW_GAME = 'y'
GUI = 'n'
ROOT = tk.Tk()


def choose_game():
    global GUI, ROOT

    choice = input(
        'choose one of the following \n1.Play against the computer \n2.Play a 2 player game\n3.Play against the computer with a GUI\nor press 0 to '
        'Exit\n').lower()
    try:
        choice1 = int(choice)
        if choice1 == 0:
            print('Have a good day \nsee you next time!')
            return choice1
        elif choice1 == 1:
            while NEW_GAME != 'n':
                comp = computer_game()
                if comp == 0:
                    break

        elif choice1 == 2:
            while NEW_GAME != 'n':
                player = player_game()
                if player == 0:
                    break
        elif choice1 == 3:
            GUI = 'y'
            gui_game()
            return
        else:
            print('Invalid choice')
            choose_game()
    except Exception as e:
        if choice == 'computer'.lower():
            computer_game()
        elif choice == 'player'.lower():
            player_game()
        else:
            print('Invalid choice')
            choose_game()


def player1_choice(choice=''):
    play = True
    while play != 0:
        print('Player 1:')
        if choice == '':
            choice = input('Choose one of the following \n1.Rock \n2.Paper \n3.Scissors\nor press 0 to Exit\n').lower()
        try:
            choice1 = int(choice)
            if choice1 == 0:
                print('Have a good day \nsee you next time!')
                play = False
                return choice1
            elif choice1 == 1:
                return print_user_choice(choice1)
            elif choice1 == 2:
                return print_user_choice(choice1)
            elif choice1 == 3:
                return print_user_choice(choice1)
            else:
                print('Invalid choice')
        except Exception:
            choice1 = 0
            if choice == 'Rock'.lower():
                choice1 = 1
                return print_user_choice(choice1)
            elif choice == 'Paper'.lower():
                choice1 = 2
                return print_user_choice(choice1)
            elif choice == 'Scissors'.lower():
                choice1 = 3
                return print_user_choice(choice1)
            else:
                print('Invalid choice')


def player2_choice():
    play = True
    while play != 0:
        print('Player 2:')
        choice = input('Choose one of the following \n1.Rock \n2.Paper \n3.Scissors\nor press 0 to Exit\n').lower()
        try:
            choice1 = int(choice)
            if choice1 == 0:
                print('Have a good day \nsee you next time!')
                play = False
                return choice1
            elif choice1 == 1:
                return print_user_choice(choice1)
            elif choice1 == 2:
                return print_user_choice(choice1)
            elif choice1 == 3:
                return print_user_choice(choice1)
            else:
                print('Invalid choice')
        except Exception:
            choice1 = 0
            if choice == 'Rock'.lower():
                choice1 = 1
                return print_user_choice(choice1)
            elif choice == 'Paper'.lower():
                choice1 = 2
                return print_user_choice(choice1)
            elif choice == 'Scissors'.lower():
                choice1 = 3
                return print_user_choice(choice1)
            else:
                print('Invalid choice')


def computer_choice():
    random.seed(time.time())
    rand = random.choice(GAME_LIST)
    image = ''
    print(f'Computer chose: {rand}\n')
    rock_img = ImageTk.PhotoImage(
        Image.open("C:\\Users\\chana\\OneDrive\\Documents\\Homwork Cyber defence course\\rock.jpg").resize((100, 100)))
    paper_img = ImageTk.PhotoImage(
        Image.open('C:\\Users\\chana\\OneDrive\\Documents\\Homwork Cyber defence course\\paper.jpg').resize((100, 100)))
    scissors_img = ImageTk.PhotoImage(
        Image.open('C:\\Users\\chana\\OneDrive\\Documents\\Homwork Cyber defence course\\scissors.jpg').resize(
            (100, 100)))
    if GAME_LIST.index(rand) == 0:
        print_rock()
        image = rock_img
    elif GAME_LIST.index(rand) == 1:
        print_paper()
        image = paper_img
    elif GAME_LIST.index(rand) == 2:
        print_scissors()
        image = scissors_img

    return rand, image


def print_user_choice(choice):
    print(f'you chose : {GAME_LIST[choice - 1]}')
    if choice - 1 == 0:
        print_rock()
    elif choice - 1 == 1:
        print_paper()
    elif choice - 1 == 2:
        print_scissors()
    return GAME_LIST[choice - 1]


def computer_game(choice=''):
    global USR_POINTS, COMUTER_POINTS, GAMES_PLAYED, NEW_GAME
    if NEW_GAME == 'y':

        user = player1_choice(choice)
        if user == 0:
            return 0
        if user != 0:
            GAMES_PLAYED += 1
            computer_l = computer_choice()
            computer = computer_l[0]
            if user == computer:
                print('Draw')
            elif user != computer:
                if GAME_LIST.index(user) - GAME_LIST.index(computer) == 1 or GAME_LIST.index(user) - GAME_LIST.index(
                        computer) == -2:
                    print('You win!')
                    USR_POINTS += 1
                else:
                    print('You loose!')
                    COMUTER_POINTS += 1

        new_game_computer()


def player_game():
    global USR_POINTS, PLAYER2_POINTS, GAMES_PLAYED, NEW_GAME
    if NEW_GAME == 'y':
        player1 = player1_choice()
        player2 = player2_choice()
        if player1 == 0 or player2 == 0:
            return 0
        if player1 != 0 or player2 != 0:
            GAMES_PLAYED += 1

            if player1 == player2:
                print('Draw')
            elif player1 != player2:
                if GAME_LIST.index(player1) - GAME_LIST.index(player2) == 1 or GAME_LIST.index(
                        player1) - GAME_LIST.index(player2) == -2:
                    print('You win!')
                    USR_POINTS += 1
                else:
                    print('You loose!')
                    PLAYER2_POINTS += 1

            new_game_player()


def new_game_computer(again=''):
    global USR_POINTS, COMUTER_POINTS, GAMES_PLAYED, NEW_GAME, GUI
    if GUI == 'n':
        again = input('Do you want to play again? y/n\n').lower()
    elif GUI == 'y':
        clear_labels(user_choice_label, computer_choice_label, result_label, points_label)

    while True:
        try:
            if again == 'y':
                print(
                    f'Games Played:{GAMES_PLAYED}\nTotal points of games for you: {USR_POINTS}\nTotal points of games '
                    f'for the computer: {COMUTER_POINTS}')
                if GUI == 'y':

                    points_label.config(
                        text=f'Games Played:{GAMES_PLAYED}\nTotal points of games for you: {USR_POINTS}\nTotal points of games '
                             f'for the computer: {COMUTER_POINTS}')
                    new_game.config(state=tk.DISABLED)
                    no_game.config(state=tk.DISABLED)
                    gui_game()

                    break
                else:
                    computer_game()
                    break
            elif again == 'n':
                points = comp_points()
                if GUI == 'y':
                    new_game.config(state=tk.DISABLED)
                    no_game.config(state=tk.DISABLED)
                    points_label1 = tk.Label(ROOT, text='', font=('Arial', 16))
                    points_label1.grid(row=4, column=0, columnspan=3, padx=10, pady=10)
                    points_label1.config(text=f'{points}')
                NEW_GAME = 'n'
                break

            else:
                print('Invalid choice')
                new_game_computer()
                break
        except Exception as e:
            print(f'Invalid choice! Error: {e}')
            again = input('Do you want to play again? y/n\n').lower()



def new_game_player():
    global USR_POINTS, PLAYER2_POINTS, GAMES_PLAYED, NEW_GAME
    again = input('Do you want to play again? y/n\n').lower()
    while True:

        try:
            if again == 'y':
                print(f'Games Played:{GAMES_PLAYED}\nTotal points of games for you: {USR_POINTS}\nTotal points of '
                      f'games for the 2nd Player: {PLAYER2_POINTS}')
                player_game()
                break
            elif again == 'n':
                player_points()

                NEW_GAME = 'n'
                break
            else:
                while True:
                    print('Invalid choice')
                    again = input('Do you want to play again? y/n\n').lower()
                    if again == 'y' or again == 'n':
                        break

        except Exception as e:
            print(f'Invalid choice! Error: {e}')
            again = input('Do you want to play again? y/n\n').lower()


def comp_points():
    global USR_POINTS, COMUTER_POINTS, GAMES_PLAYED, NEW_GAME, GUI
    if USR_POINTS > COMUTER_POINTS:
        print(
            f'Games Played:{GAMES_PLAYED}\nYou Won!! with the Total points of {USR_POINTS}\nThe computer got {COMUTER_POINTS}')

        # NEW_GAME = 'n'
        return f'Games Played:{GAMES_PLAYED}\nYou Won!! with the Total points of {USR_POINTS}\nThe computer got {COMUTER_POINTS}'
    elif USR_POINTS == COMUTER_POINTS:
        print(f'Games Played:{GAMES_PLAYED}\nIts a Draw!\nYour Total points of {USR_POINTS}')
        # NEW_GAME = 'n'
        return f'Games Played:{GAMES_PLAYED}\nIts a Draw!\nYour Total points is {USR_POINTS}'
    else:
        print(
            f'Games Played:{GAMES_PLAYED}\nYou Lost with the Total points of {USR_POINTS}\nThe computer got {COMUTER_POINTS}')
        # NEW_GAME = 'n'
        return f'Games Played:{GAMES_PLAYED}\nYou Lost with the Total points of {USR_POINTS}\nThe computer got {COMUTER_POINTS}'


def player_points():
    global USR_POINTS, PLAYER2_POINTS, GAMES_PLAYED, NEW_GAME
    if USR_POINTS > PLAYER2_POINTS:
        print(f'You Won!! with the Total points of {USR_POINTS}\nPlayer 2 got {PLAYER2_POINTS}')
        # NEW_GAME = 'n'
        return f'You Won!! with the Total points of {USR_POINTS}\nPlayer 2 got {PLAYER2_POINTS}'
    elif USR_POINTS == COMUTER_POINTS:
        print(f'Its a Draw!\nYour Total points of {USR_POINTS}')
        # NEW_GAME = 'n'
        return f'Its a Draw!\nYour Total points of {USR_POINTS}'
    else:
        print(f'You Lost with the Total points of {USR_POINTS}\nPlayer 2 got {PLAYER2_POINTS}')
        # NEW_GAME = 'n'
        return f'You Lost with the Total points of {USR_POINTS}\nPlayer 2 got {PLAYER2_POINTS}'


def print_rock():
    print("""
                _______
            ---'   ____)
                  (_____)
                  (_____)
                  (____)
            ---._____(___)
            """)


def print_paper():
    print("""
             _______
        ---'    ____)____
                   ______)
                  _______)
                 _______)
        ---.__________)
        """)


def print_scissors():
    print("""
            _______
        ---'   ____)____
                  ______)
               __________)
              (____)
        ---.__(___)
        """)


def gui_game():
    global user_choice_label, computer_choice_label, computer_choice_image, result_label, new_game_label, points_label, rock_btn, scissors_btn, paper_btn
    global NEW_GAME, ROOT

    ROOT.title('Rock Paper Scissors')

    # Load images
    rock_img = ImageTk.PhotoImage(
        Image.open("C:\\Users\\chana\\OneDrive\\Documents\\Homwork Cyber defence course\\rock.jpg").resize((100, 100)))
    paper_img = ImageTk.PhotoImage(
        Image.open('C:\\Users\\chana\\OneDrive\\Documents\\Homwork Cyber defence course\\paper.jpg').resize((100, 100)))
    scissors_img = ImageTk.PhotoImage(
        Image.open('C:\\Users\\chana\\OneDrive\\Documents\\Homwork Cyber defence course\\scissors.jpg').resize(
            (100, 100)))

    # Create buttons for user choices
    rock_btn = tk.Button(ROOT, text='Rock', image=rock_img, width=50, command=lambda: on_button_click('rock'))
    rock_btn.grid(row=1, column=0, padx=10, pady=10)

    paper_btn = tk.Button(ROOT, text='Paper', image=paper_img, width=50, command=lambda: on_button_click('paper'))
    paper_btn.grid(row=1, column=1, padx=10, pady=10)

    scissors_btn = tk.Button(ROOT, text='Scissors', image=scissors_img, width=50,
                             command=lambda: on_button_click('scissors'))
    scissors_btn.grid(row=1, column=2, padx=10, pady=10)

    # Create labels to display choices and result
    user_choice_label = tk.Label(ROOT, font=('Arial', 12))
    user_choice_label.grid(row=0, padx=10, pady=10)

    result_label = tk.Label(ROOT, text='', font=('Arial', 16))
    result_label.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

    points_label = tk.Label(ROOT, text='', font=('Arial', 16))
    points_label.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

    computer_choice_label = tk.Label(ROOT, text='', font=('Arial', 12))
    computer_choice_label.grid(row=5, columnspan=3, padx=10, pady=10)

    computer_choice_image = tk.Label(ROOT)
    computer_choice_image.grid(row=6, column=2, rowspan=1, padx=10, pady=10)

    new_game_label = tk.Label(ROOT, text='')
    new_game_label.grid(row=7, column=0, columnspan=3, padx=10, pady=10)
    # Run the application
    ROOT.mainloop()


def on_button_click(choice):
    global USR_POINTS, COMUTER_POINTS, GAMES_PLAYED, NEW_GAME, GUI, new_game, no_game
    clear_labels(user_choice_label, computer_choice_label, result_label, points_label)

    user_choice = choice

    if NEW_GAME == 'y':

        user = player1_choice(user_choice)
        if user == 0:
            return 0
        if user != 0:
            GAMES_PLAYED += 1
            computer_l = computer_choice()
            computer = computer_l[0]

            user_choice_label.config(text=f"You chose: {user_choice}", font=('Arial', 12))
            computer_choice_label.config(text=f'Computer Chose: {computer}', font=('Arial', 12))
            computer_choice_image.config(image=computer_l[1])
            computer_choice_image.image = computer_l[1]
            if user == computer:

                result_label.config(text='Draw', font=('Arial', 16))
            elif user != computer:

                if GAME_LIST.index(user) - GAME_LIST.index(computer) == 1 or GAME_LIST.index(user) - GAME_LIST.index(
                        computer) == -2:
                    result_label.config(text='You win!', font=('Arial', 16))
                    USR_POINTS += 1

                else:
                    result_label.config(text='You loose!', font=('Arial', 16))

                    COMUTER_POINTS += 1

    rock_btn.config(state=tk.DISABLED)
    paper_btn.config(state=tk.DISABLED)
    scissors_btn.config(state=tk.DISABLED)

    new_game_label.config(text='Do you want to play a again?', font=('Arial', 12))

    new_game = tk.Button(ROOT, text='yes', width=30, command=lambda: new_game_computer('y'))
    new_game.grid(row=8, column=0, columnspan=1, padx=10, pady=10)

    no_game = tk.Button(ROOT, text='no', width=30, command=lambda: new_game_computer('n'))
    no_game.grid(row=8, column=1, columnspan=2, padx=10, pady=10)


def clear_labels(user_choice_label, computer_choice_label, result_label, points_label):
    user_choice_label.config(text='', font=('Arial', 12))
    computer_choice_label.config(text='', font=('Arial', 16))
    result_label.config(text='', font=('Arial', 16))
    points_label.config(text='', font=('Arial', 16))


if __name__ == '__main__':

    while True:

        game = choose_game()
        if game == 0:
            break
        diff_game = input('Do You want to exit the program?  y/n \n').lower()
        try:
            if diff_game == 'y':
                break
            elif diff_game == 'n':
                pass
            elif diff_game != 'y' and diff_game != 'n':
                while True:
                    print('Invalid choice! ')
                    diff_game = input('Do You want to exit the program?  y/n \n').lower()
                    if diff_game == 'y' or diff_game == 'n':
                        break
        except Exception as e:
            print(f'Invalid choice! Error: {e}')
        game = ()
        GAMES_PLAYED = 0
        NEW_GAME = 'y'
        ROOT = tk.Tk()
