from sys import exit


def dead(why):
    print(why, "Good job!")
    exit(0)


def gold_room():
    print("This room is full of gold. How much do you take?")
    exit(0)

bear_moved = False
while True:
    next = input('>')
    if next == 'take honey':
        dead("The bear looks at you then slaps your face off.")
    elif next == "taunt bear" and not bear_moved:  # true and ture=true
        print("The bear has moved from the door. You can go through it now.")
        bear_moved = True
    elif next == "taunt bear" and bear_moved:  # true and false= false
        dead("The bear gets pissed off and chews your leg off.")
    elif next == "open door" and bear_moved:
        gold_room()
    else:
        print("I got no idea what that means.")
