
from board import Board
from constants import *

board = None

def observePlay(me):
    global board

    hasAsked = False
    hasSuspect = False
    hasWeapon = False
    hasRoom = False

    while not hasAsked:
        # get current player
        print(", ".join(board.playerNames))
        currentPlayer = input("Asking Who? ")

        if currentPlayer not in board.playerNames:
            print(f"{currentPlayer} is not a player")
            continue

        asked = board.playerNames.index(currentPlayer)

        hasAsked = True

    while not hasSuspect:
        print(", ".join(suspects))
        suspect = input("Suspect: ")

        if suspect not in suspects:
            print(f"{suspect} not a suspect")
            continue

        hasSuspect = True

    while not hasWeapon:
        print(", ".join(weapons))
        weapon = input("Weapon: ")

        if weapon not in weapons:
            print(f"{weapon} not a weapon")
            continue

        hasWeapon = True

    while not hasRoom:
        print(", ".join(rooms))
        room = input("Room: ")

        if room not in rooms:
            print(f"{room} not a room")
            continue

        hasRoom = True

    if me:
        hasCard = False
        while not hasCard:
            card = input("Card Shown (n if none): ")
            if card == "n":
                board.observePlay(asked, suspect, weapon, room, False)
                return
            if not board.isCard(card):
                print(f"{card} not valid input")
                continue
            board.playerHasCard(asked, card)
            hasCard = True
    else:
        output = input("Did they have a card (y/n): ")
        hadCard = output == "y"
        board.observePlay(asked, suspect, weapon, room, hadCard)



if __name__ == "__main__":
    # numPlayers = int(input("Number of Players: "))
    # board = Board(numPlayers)
    # name = input("Enter your name: ")
    # numMyCards = int(input("Number of Cards: "))
    # board.playerNames[0] = name
    # board.numCards[0] = numMyCards

    # for i in range(numPlayers-1):
    #     name = input("Enter new player name: ")
    #     numCards = int(input("Number of Cards: "))
    #     board.playerNames[i+1] = name
    #     board.numCards[i+1] = numCards

    # board.printBoard()

    # isRunning = True

    # myCards = []
    # for i in range(numMyCards):
    #     hasCard = False
    #     while not hasCard:
    #         card = input("New Card: ")
    #         if not board.isCard(card):
    #             print(f"{card} not a card")
    #             continue

    #         myCards.append(card)
    #         hasCard = True

    # 

    numPlayers = 3
    board = Board(numPlayers)
    board.playerNames[0] = "Declan"
    board.numCards[0] = 6
    board.playerNames[1] = "Phelan"
    board.numCards[1] = 6
    board.playerNames[2] = "Kieran"
    board.numCards[2] = 6
    
    numMyCards = 3
    MyCards = [
        "Mrs. Peacock",
        "Colonel Mustard",
        "Lead Pipe",
        "Kitchen",
        "Ballroom",
        "Conservatory"
    ]

    # Keep
    board.myCards(MyCards)

    # board.observePlay(1, "Mr. Green", "Knife", "Billiard Room", True)
    # board.observePlay(1, "Mr. Green", "Wrench", "Study", True)
    # board.printBoard()
    # board.observePlay(1, "Mrs. Peacock", "Wrench", "Billiard Room", False)
    # board.observePlay(1, "Professor Plum", "Knife", "Hall", False)

    # board.observePlay(1, "Miss Scarlet", "Knife", "Hall", False)
    # board.observePlay(1, "Professor Plum", "Wrench", "Study", False)
    # board.observePlay(1, "Mrs. White", "Revolver", "Billiard Room", False)



    while not board.isGameOver:
        # get current player
        board.printBoard()
        output = input("Is your turn (y/n): ")
        me =  output == "y"
        observePlay(me)
