import json

from constants import suspects, weapons, rooms

class Board:

    def __init__(self, numPlayers):
        # 0 is Me
        self.numPlayers = numPlayers
        self.playerNames = []                   # list of strings
        self.numCards = []                      # list of ints
        self.gamestates = []                    # list of gamestates
        self.playerUnknowns = []                # list of sets of arrays
        self.posible = self.createPossible()    # dict of lists
        self.allKnown = []
        self.isGameOver = False

        for i in range(numPlayers):
            self.playerNames.append("")
            self.numCards.append(-1)
            self.gamestates.append(self.createState())
            self.playerUnknowns.append([])
            self.allKnown.append(False)
        
    def createPossible(self):
        # create a set of posible options
        possible = {
            "suspects": suspects[:],
            "weapons": weapons[:],
            "rooms": rooms[:]
        }
        return possible
    
    def createState(self):
        # create the struct for each user
        state = {
            "suspects": {},
            "weapons": {},
            "rooms": {}
        }

        # -1 unknown
        # 0  does not have it
        # 1  has it
        for sus in suspects:
            state["suspects"][sus] = -1
        for wep in weapons:
            state["weapons"][wep] = -1
        for room in rooms:
            state["rooms"][room] = -1

        return state

    def createPlayerUnknown(self, player, suspect, weapon, room):
        unknown = []
        # check if possible
        if suspect in self.posible["suspects"]:
            if self.gamestates[player]["suspects"][suspect] == -1: 
                # TODO: second if should be redundent 
                unknown.append(suspect)
        if weapon in self.posible["weapons"]:
            if self.gamestates[player]["weapons"][weapon] == -1: 
                # TODO: second if should be redundent 
                unknown.append(weapon)
        if room in self.posible["rooms"]:
            if self.gamestates[player]["rooms"][room] == -1: 
                # TODO: second if should be redundent 
                unknown.append(room)

        if len(unknown) == 0:
            # learned nothing
            print("\tleanred nothing")
            return False

        # check if one left
        if len(unknown) == 1:
            # player must then have this card
            return self.playerHasCard(player, unknown[0])
            
        
        # else create an unknown
        unknown = tuple(unknown)

        # TODO: handle if unknown already exists
        self.playerUnknowns[player].append(unknown)
        print(f"\tcreated unknown")
        return False

    def setPlayer(self, number, name, numCards):
        # set data for a player
        self.playerNames[number] = name
        self.numCards[number] = numCards

    def myCards(self, cards):
        # set data for my cards
        for card in cards:
            self.playerHasCard(0, card)
        pass

    def observePlay(self, asked, suspect, weapon, room, had_a_card):
        # witness a question from another
        if not had_a_card:
            a = self.playerDoesNotHaveCard(asked, suspect)
            b = self.playerDoesNotHaveCard(asked, weapon)
            c = self.playerDoesNotHaveCard(asked, room)
            return a or b or c
        else:
            return self.createPlayerUnknown(asked, suspect, weapon, room)
        
    def playerHasCard(self, player, card):
        # Player has a known card 
        print(f"\t{self.playerNames[player]} has the {card} Card")

        # adjust gamestate
        cardType = self.getCardType(card)
        if cardType == "error":
            return False
        self.gamestates[player][cardType][card] = 1

        # change possible 
        self.posible[cardType].remove(card)

        # remove unknows with this 
        unknowns = self.playerUnknowns[player]
        for unknown in unknowns:
            if card in unknown:
                self.playerUnknowns[player].remove(unknown)

        # Other players cannot have it
        for i in range(self.numPlayers):
            if i != player:
                self.gamestates[i][cardType][card] = 0

        # check win condition
        self.checkFoundAll()
        return self.checkWin()

    def playerDoesNotHaveCard(self, player, card):
        # Player does not have a known card
        print(f"\t{self.playerNames[player]} does not have the {card}")

        # adjust gameste
        cardType = self.getCardType(card)
        if cardType == "error":
            return False
        self.gamestates[player][cardType][card] = 0

        # remove from unknowns
        numUnknowns = len(self.playerUnknowns[player])
        for i in range(numUnknowns):
            if card in self.playerUnknowns[player][i]:
                unknown = self.playerUnknowns[player].pop(i)
                toList = list(unknown)
                toList.remove(card)
                # only one left
                if len(toList) == 1:
                    self.playerHasCard(player, toList[0])
                else:
                    self.playerUnknowns[player].append(tuple(toList))

        # check win condition
        self.checkFoundAll()
        return self.checkWin()
    
    def doesPlayerHaveCard(self, player, card, hasCard):
        # sets if a player has or does not have a known card
        if hasCard:
            return self.playerHasCard(player, card)
        else:
            return self.playerDoesNotHaveCard(player, card)

    def getCardType(self, card):
        # get the type from the card
        if card in suspects:
            return "suspects"
        if card in weapons:
            return "weapons"
        if card in rooms:
            return "rooms"
        return "error"
    
    def isCard(self, card):
        # get if its a card or not
        return card in suspects or card in weapons or card in rooms

    def checkFoundAll(self):
        # check if all cards are known for players
        for i in range(self.numPlayers):

            if self.allKnown[i]:
                # all cards already known for this player
                continue

            numKnown = 0
            numUnknown = 0
            total = len(suspects) + len(weapons) + len(rooms)
            numPlayerCards = self.numCards[i]
            value = None

            # count the known and unknown
            for suspect in suspects:
                if self.gamestates[i]["suspects"][suspect] == 0:
                    numUnknown += 1
                elif  self.gamestates[i]["suspects"][suspect] == 1:
                    numKnown += 1
            for weapon in weapons:
                if self.gamestates[i]["weapons"][weapon] == 0:
                    numUnknown += 1
                elif self.gamestates[i]["weapons"][weapon] == 1:
                    numKnown += 1
            for room in rooms:
                if self.gamestates[i]["rooms"][room] == 0:
                    numUnknown += 1
                if self.gamestates[i]["rooms"][room] == 1:
                    numKnown += 1

            # if all players cards are known
            if numKnown == numPlayerCards:
                # We found all their cards, rest they don't have
                value = False
                self.allKnown[i] = True

            # if all players not cards are known
            if numUnknown == total - numPlayerCards:
                # We know all cards they don't have, rest they have 
                value = True
                self.allKnown[i] = True

            # check if we hit anything
            if value == None:
                return
            
            print(f"\tAll Cards Known for {self.playerNames[i]}")

            # fill in missing info
            for suspect in suspects:
                if self.gamestates[i]["suspects"][suspect] == -1:
                    self.doesPlayerHaveCard(i, suspect, value)
            for weapon in weapons:
                if self.gamestates[i]["weapons"][weapon] == -1:
                    self.doesPlayerHaveCard(i, weapon, value)
            for room in rooms:
                if self.gamestates[i]["rooms"][room] == -1:
                    self.doesPlayerHaveCard(i, room, value)

    def checkWin(self):
        self.posible
        if (len(self.posible["suspects"]) == 1 and
            len(self.posible["weapons"]) == 1 and 
            len(self.posible["rooms"]) == 1):

            suspect = self.posible["suspects"][0]
            weapon = self.posible["weapons"][0]
            room = self.posible["rooms"][0]
            print("I Know the Killer!!")
            print(f"\tIt was {suspect} with the {weapon} in the {room}")
            self.isGameOver = True
            return True
        return False
        

    def printBoard(self):
    
        numPlayers = len(self.playerNames)
        cellSize = 8
        lableCellSize = 17
        prt = ""
        row = ""
        c = "|"
        r = "-"* cellSize
        lr = "-"* lableCellSize
        
        # Print names
        prt = c + " "*lableCellSize + c
        filler = c + lr + c
        for name in self.playerNames:
            prt = prt + name.ljust(cellSize) + c
            filler = filler + r + c
        
        filler = filler + "\n"
        prt = prt + "\n" + filler

        def displayUnknowns(player, card):
            disp = []
            unknowns = self.playerUnknowns[player]
            for index, unknown in enumerate(unknowns):
                if card in unknown:
                    disp.append(str(index))

            return ",".join(disp)

        # print cells
        def printCell(player, group, card):
            status = self.gamestates[player][group][card]
            if status == -1:
                # unknown
                dispUnknowns = displayUnknowns(player, card)
                return dispUnknowns.ljust(cellSize) + c
            elif status == 0:
                return "^"*cellSize + c
            elif status == 1:
                return " [HAS]".ljust(cellSize) + c
            return "Error"

        def isPossible(group, card):
            if card in self.posible[group]:
                return "  "
            else:
                return "X "
            
        def labelCell(group, card):
            value = isPossible(group, card) + card
            return c + value.ljust(lableCellSize) + c

        # print suspects
        for sus in suspects:
            row = labelCell("suspects", sus)
            for i in range(numPlayers):
                row = row + printCell(i, "suspects", sus)    
            prt = prt + row + "\n"
        prt = prt + filler

        # print weapons
        for weapon in weapons:
            row = labelCell("weapons", weapon)
            for i in range(numPlayers):
                row = row + printCell(i, "weapons", weapon)  
            prt = prt + row + "\n"
        prt = prt + filler

        # print rooms
        for room in rooms:
            row = labelCell("rooms", room)
            for i in range(numPlayers):
                row = row + printCell(i, "rooms", room)    
            prt = prt + row + "\n"
        prt = prt + filler

        # for each player print if they have it

        print(prt)
        return
    