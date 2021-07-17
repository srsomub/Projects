import random
"""SNAKE WATER GUN GAME"""

C1 = 0
D1 = 0
Y1 = 0
C2 = 0
Y2 = 0
D2 = 0
C3 = 0
D3 = 0
Y3 = 0
a=0
def game():



       

        b = ["Snake", "Water", "Gun"]
        

        def Snake():
            global C1,D1,Y1 , n , a


            a = random.choice(b)
            print(f"Computer choose : {a} \n")

            if (a != "Snake"):
                if (a == "Water"):
                    print("Soryy you loose")
                    C1 += 1

                else:
                    print("Congrats you won")
                    Y1 += 1

            else:
                print("Match draw")
                D1+=1

            print("\nWant to play again \n1:Yes\n2:No :")
            A = int(input("Your choice: "))

            if (A == 1):

                game()
            elif (A == 2):
                print("Thanks for playing game")
                print(f"\nYou won {Y1+Y2+Y3} times , Computer won {C1+C2+C3} times and Draw occured {D1+D2+D3} times ")

            else:
                print("Enter valid number")

        def Water():
            global C2,D2,Y2
            a = random.choice(b)
            print(f"Computer choose : {a} \n")
            if (a != "Water"):
                if (a == "Snake"):
                    print("Soryy you loose")
                    C2 += 1

                else:
                    print("Congrats you won")
                    Y2 += 1

            else:
                print("Match draw")
                D2+=1
            print("\nWant to play again \n1:Yes\n2:No :")
            A = int(input("Your choice: "))

            if (A == 1):
                game()
            elif (A == 2):
                print("Thanks for playing game")
                print(
                    f"\nYou won {Y1 + Y2 + Y3} times , Computer won {C1 + C2 + C3} times and Draw occured {D1 + D2 + D3} times ")
                    



            else:
                print("Enter valid number")

        def Gun():
            global C3, Y3, D3

            a = random.choice(b)
            print(f"Computer choose : {a} \n")
            if (a != "Gun"):
                if (a == "Water"):
                    print("Soryy you loose")
                    C3 += 1

                else:
                    print("Congrats you won")
                    Y3 += 1


            else:
                print("Match draw")
                D3+=1

            print("\nWant to play again \n1:Yes\n2:No :")

            A = int(input("Your choice: "))

            if (A == 1):
                game()
            elif (A == 2):
                print("Thanks for playing game")
                print(
                    f"\nYou won {Y1 + Y2 + Y3} times , Computer won {C1 + C2 + C3} times and Draw occured {D1 + D2 + D3} times ")



            else:
                print("Enter valid number")

        if (x == 1):
            Snake()

        elif (x == 2):
            Water()

        elif (x == 3):
            Gun()

        else :
            print("Enter number from 1 to 3")






start = {"1": "Snake\n", "2": "Water\n", "3": "Gun"}

    

for i, j in start.items():
            print(f"Press {i} for {j}", end="")
try:
            x = int(input("\nEnter your choice : "))
            game()
except Exception as e:
            print(f"{e}")
