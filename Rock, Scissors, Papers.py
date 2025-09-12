import random

dict = {1:"Rock", 2:"Scissors", 3:"Paper"}

user_input = int(input())
computer_input = random.randint(1, 3)

print(f"Human Chooses {dict[user_input]}\nComputer Chooses {dict[computer_input]}")

if computer_input == user_input:
    print("Tie!")
elif user_input == 1 and computer_input == 2:
    print("You Win!")
elif user_input == 2 and computer_input == 3:
    print("You Win!")
elif user_input == 3 and computer_input == 1:
    print("You Win!")
else:
    print("Computer Wins!")
