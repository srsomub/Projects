"""
Name : Somu Srinivas Budidha

Project 2 : Build Tic-Tac-Toe game using Python

"""

player = 1        
total_moves = 9     
val = {
    '7': ' ', '8': ' ', '9': ' ',
    '4': ' ', '5': ' ', '6': ' ',
    '1': ' ', '2': ' ', '3': ' '
}   # Creating a empty value dictionary
def check():
    if ((val['1'] == 'X' and val['2'] == 'X' and val['3'] == 'X') or (val['4'] == 'X' and val['5'] == 'X' and val['6'] == 'X') or (val['7'] == 'X' and val['8'] == 'X' and val['9'] == 'X') or (val['1'] == 'X' and val['5'] == 'X' and val['9'] == 'X') or (val['7'] == 'X' and val['5'] == 'X' and val['3'] == 'X') or (val['1'] == 'X' and val['4'] == 'X' and val['7'] == 'X') or (val['2'] == 'X' and val['5'] == 'X' and val['8'] == 'X') or (val['3'] == 'X' and val['6'] == 'X' and val['9'] == 'X')):
        print(f'Congratulations, {name1.capitalize()} you won this game !!!!!')
        print()

        return 1  
    elif ((val['1'] == 'O' and val['2'] == 'O' and val['3'] == 'O') or (val['4'] == 'O' and val['5'] == 'O' and val['6'] == 'O') or (val['7'] == 'O' and val['8'] == 'O' and val['9'] == 'O') or (val['1'] == 'O' and val['5'] == 'O' and val['9'] == 'O') or (val['7'] == 'O' and val['5'] == 'O' and val['3'] == 'O') or (val['1'] == 'O' and val['4'] == 'O' and val['7'] == 'O') or (val['2'] == 'O' and val['5'] == 'O' and val['8'] == 'O') or (val['3'] == 'O' and val['6'] == 'O' and val['9'] == 'O')):
            print(f'Congratulations, {name2.capitalize()} you won this game !!!!!')
            print()
            return 1
    else:
        return 0
print()
print()
print("                                  **********     Welcome to LetsUpgrade Tic-Tac-Toe gaming zone     **********\n")
print('                                                                .-----------------.')
print('                                                                |  7  |  8  |  9  |')
print('                                                                |-----|-----|-----|')
print('                                                                |  4  |  5  |  6  |')
print('                                                                |-----|-----|-----|')
print('                                                                |  1  |  2  |  3  |')
print('                                                                *-----------------*')
print("\n")
print("1st Player will choose 'X and 2nd Player will choose 'O' ")
name1=input("Enter 1st player name : ")
name2=input("Enter 2nd player name : ")
print()
print(f"Player {name1.capitalize()} choosed X")
print(f"Player {name2.capitalize()} choosed O")
print()
print("\n* Enter Any Number according to above box * \n")
print("Let's Begin our Game")

a=True

while a:
    
        print('                                                               .-----------------.')
        print('                                                               |  {0}  |  {1}  |  {2}  |'.format(val['7'],val['8'],val['9']))
        print('                                                               |-----|-----|-----|')
        print('                                                               |  {0}  |  {1}  |  {2}  |'.format(val['4'],val['5'],val['6']))
        print('                                                               |-----|-----|-----|')
        print('                                                               |  {0}  |  {1}  |  {2}  |'.format(val['1'],val['2'],val['3']))
        print('                                                               *-----------------*')
        
        res=check()   # Creating an object of check() , which returns desire values required for game
        if res==0:
            if (total_moves>0): # terminate the game if total moves become more than 9
                print(f"{total_moves} moves are remaining to end")
                if(player==1):
                    p1_input = input(f'{name1.capitalize()} your turn : ')
                    if p1_input in val and val[p1_input] == ' ':  # check whether desired location is available or not
                                    val[p1_input] = 'X'     # if available then the value get added to the located key 
                                    player=2
                                    total_moves-=1
                                    
                                    
                
                    else:
                        print('Invalid input, please try again')
                        continue
                else:                                       #       for player 2
                        p2_input = input(f'{name2.capitalize()} your turn : ')
                        if p2_input in val and val[p2_input] == ' ':
                            val[p2_input] = 'O'
                            player = 1
                            total_moves-=1
                         
                            
                        else:
                            print('Invalid input, please try again')
                            continue
            else:
                print(f"Match Draw !\nThankyou, {name1.capitalize()} & {name2.capitalize()} for enjoying this game")
                print()
                a=False
        else:               # indicating , Someone  has Won the Game
            break


        