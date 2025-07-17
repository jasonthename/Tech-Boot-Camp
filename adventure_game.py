#This should work without needing to install anything extra

print("You're in a dark forest. Left or Right?")
choice = input("Which path? ")

if choice.lower() == "left":
    print("You found a treasure chest!")
else:
    print("A wild bear chases you!")