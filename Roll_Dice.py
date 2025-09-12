import random as rn

#int(input())
dice_count = 2
dice_return = 0

for i in range(0, dice_count):
    roll = rn.randint(1,6)
    dice_return += roll
    print(f"Roll {i+1}: {roll}")


print(f"Total: {dice_return}")
