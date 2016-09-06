import random
import DurakRulesHelperFunctions
class Game:
    def __init__(self, numPlayers):
        #initialize and shuffle deck
        self.deck = ['6♣', '7♣', '8♣', '9♣', '10♣', 'J♣', 'Q♣', 'K♣', 'A♣',\
                     '6♦', '7♦', '8♦', '9♦', '10♦', 'J♦', 'Q♦', 'K♦', 'A♦',\
                     '6♥', '7♥', '8♥', '9♥', '10♥', 'J♥', 'Q♥', 'K♥', 'A♥',\
                     '6♠', '7♠', '8♠', '9♠', '10♠', 'J♠', 'Q♠', 'K♠', 'A♠']
        random.shuffle(self.deck)
        self.trump = self.deck[0]
        #initialize players
        self.players = []
        for i in range(numPlayers):
            self.players.append(Player("Player " + str(i+1)))
            #deal hands
            for _ in range(6):
                self.players[i].addCard(self.drawCard())
        #reorder players so that the one with lowest trump goes first
        self.players = DurakRulesHelperFunctions.playOrder(self.players,self.trump[-1])
        self.MainGameLoop()

    def MainGameLoop(self):
        """Runs the game"""
        print("Welcome to Durak. The Trump card is " + self.trump)
        print("Note: when prompted for the index of a card, the indices start at 0.")
        while len(self.players) > 1:
            attacker = self.players[0] #attacker is first in the turn order
            defender = self.players[1] #defender is next
            inPlay = [] #cards that have been played this bout
            attackCount = 0
            maxAttackCount = min(len(defender.hand), 6) #maximum number of attacks is either 6 or the number of cards the defender has, whichever is smaller
            attack = attacker.promptFirstAttack(defender)
            inPlay.append(attack) #add card to field
            attackCount += 1
            defence = defender.promptDefence(attacker, attack, self.trump)
            while defence != "" and attack != "":
                inPlay.append(defence)
                print(defender.name + " has defended with a " + defence + ". The cards currently in play are:")
                print(inPlay)
                attack = attacker.promptFollowupAttack(defender, inPlay, attackCount, maxAttackCount)
                if attack == None: #if the attacker has chosen to let others attack
                    assist = ""
                    for assistant in self.players[2:]: #other players get a chance to attack, in turn order
                        assist = assistant.promptAssistAttack(attacker, defender, inPlay, attackCount, maxAttackCount)
                        if assist != "": #first other player in turn order to make an attack is the assistant
                            inPlay.append(assist) #add card to field
                            attackCount += 1
                            defence = defender.promptDefence(assistant, assist, self.trump)
                            break
                    attack = assist
                elif attack != "": #if the attacker attacked
                    inPlay.append(attack) #add card to field
                    attackCount += 1
                    defence = defender.promptDefence(attacker, attack, self.trump)
            if defence == "": #defender has chosen not to defend
                print(defender.name + " has conceded the attack.")
                for player in [self.players[0]]+self.players[2:]:
                    dumpedCards = player.promptDumpExtraCards(defender, inPlay, attackCount, maxAttackCount)
                    inPlay += dumpedCards
                    attackCount += len(dumpedCards)
                print("The following cards have been added to " + defender.name + "'s hand:")
                print(inPlay)
                defender.hand += inPlay #if the defender concedes, add cards in play to their hand
                for player in self.players: #all players draw cards until they have 6, starting at the attacker, so long as there are cards in the deck
                    if len(player.hand) < 6:
                        for _ in range(min(6 - len(player.hand), len(self.deck))):
                            player.addCard(self.drawCard())
                self.players = self.players[2:] + self.players[:2] #defenders turn is skipped if they concede
            if attack == "": #attacker has chosen to stop attacking
                print("The attack has ended. the following cards have been removed from play:")
                print(inPlay)
                for player in self.players: #all players draw cards until they have 6, starting at the attacker, so long as there are cards in the deck
                    if len(player.hand) < 6:
                        for _ in range(min(6 - len(player.hand), len(self.deck))):
                            player.addCard(self.drawCard())
                self.players = self.players[1:] + self.players[:1] #attacker moves to end of turn order, defender attacks next
            self.players = list(filter(lambda x: len(x.hand) != 0, self.players)) #remove players who have run out of cards
        if len(self.players) == 1: #if only one player has cards, they are the loser
            print(self.players[0].name + " is the only player still holding cards! They are the Durak!")
        if len(self.players) == 0: #if all players have run out of cards, game is a draw
            print("No one has any cards left! This round is a draw.")
                                                

    def drawCard(self):
        """Removes the last card in the deck and returns its value"""
        if self.deck != []:
            dealtCard = self.deck[-1]
            self.deck = self.deck[:-1]
            return dealtCard


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def addCard(self, card):
        """Adds a card to the hand"""
        if card != None:
            self.hand.append(card)

    def removeCard(self, index):
        """Removes the card at the given index from the hand"""
        self.hand = self.hand[:index] + self.hand[index+1:]

    def promptFirstAttack(self, defender):
        """Asks player to chose a card to begin a bout"""
        print(self.name + "'s turn to attack " + defender.name +\
              ". Please select a card.")
        print(self.name + "'s hand:")
        print(self.hand)
        selection = input("Select the index of the card you wish to play:")
        validOptions = list(map(lambda x: str(x),range(len(self.hand)))) #creates a list of all possible indeces as strings
        while selection not in validOptions:
            selection = input("Invalid index. Select the index of the card you wish to play:")
        attack = self.hand[int(selection)]
        self.removeCard(int(selection))
        return attack

    def promptFollowupAttack(self, defender, inPlay, attackCount, maxAttackCount):
        """Asks player to choose a followup attack, and if none is chosen, asks whether assistance is allowed. Returns None if assistance is requested"""
        print(self.name + ", would you like to follow up your attack?")
        print("Select a card to continue the attack, or just press enter to stop attacking.")
        print(self.hand)
        selection = input("Select the index of the card you wish to play:")
        validOptions = list(map(lambda x: str(x),range(len(self.hand)))) + [""] #creates a list of all possible indeces as strings, plus the empty string
        while selection not in validOptions:
            selection = input("Invalid index. Select the index of the card you wish to play:")
        while selection != "" and not DurakRulesHelperFunctions.validAttack(self.hand[int(selection)], attackCount, maxAttackCount, inPlay):
            #keeps prompting until a valid attack is given, or the attacker chooses not to attack
            print(self.hand[int(selection)] + " is not a valid attack. Followup" +\
                  " attacks must be of the same value as a card that is already in play, "+\
                  "and total number of attacks must not exceed " + str(maxAttackCount) + ".")
            print("Cards in play: ", inPlay)
            selection = input("Select the index of the card you wish to play:")
            while selection not in validOptions:
                selection = input("Invalid index. Select the index of the card you wish to play:")
        if selection == "":
            if input("Would you like to allow other players to attack? (y/n)") == "y":
                return None
            else:
                return ""
        attack = self.hand[int(selection)]
        self.removeCard(int(selection))
        return attack

    def promptAssistAttack(self, attacker, defender, inPlay, attackCount, maxAttackCount):
        """Asks player to chose an assist attack"""
        print(self.name + ", would you like to follow up " + attacker.name + "'s attack?")
        print("Cards in play: ", inPlay)
        print("Select a card to continue the attack, or just press enter to stop attacking.")
        print(self.hand)
        selection = input("Select the index of the card you wish to play:")
        validOptions = list(map(lambda x: str(x),range(len(self.hand)))) + [""] #creates a list of all possible indeces as strings, plus the empty string
        while selection not in validOptions:
            selection = input("Invalid index. Select the index of the card you wish to play:")
        while selection != "" and not DurakRulesHelperFunctions.validAttack(self.hand[int(selection)], attackCount, maxAttackCount, inPlay):
            #keeps prompting until a valid attack is given, or the aassistant chooses not to assist
            print(self.hand[int(selection)] + " is not a valid attack. Followup" +\
                  " attacks must be of the same value as a card that is already in play, "+\
                  "and total number of attacks must not exceed " + str(maxAttackCount) + ".")
            print("Cards in play: ", inPlay)
            selection = input("Select the index of the card you wish to play:")
            while selection not in validOptions:
                selection = input("Invalid index. Select the index of the card you wish to play:")
        if selection == "":
                return ""
        attack = self.hand[int(selection)]
        self.removeCard(int(selection))
        return attack

    def promptDefence(self, attacker, attack, trump):
        """Asks player to defend from an attack"""
        print(attacker.name + " has attacked " + self.name +\
          " with a " + attack + ".")
        print(self.name + ", please select a card to defend, or just press enter to concede the attack.")
        print(self.hand)
        selection = input("Select the index of the card you wish to play:")
        validOptions = list(map(lambda x: str(x),range(len(self.hand)))) + [""] #creates a list of all possible indeces as strings, plus the empty string
        while selection not in validOptions:
            selection = input("Invalid index. Select the index of the card you wish to play:")
        while selection != "" and not DurakRulesHelperFunctions.validDefence(attack, self.hand[int(selection)], trump[-1]):
            #checks if the defence is valid
            print(self.hand[int(selection)] + " cannot defend against " + attack +\
                  ". Select another card, or press enter to concede the attack.")
            selection = input("Select the index of the card you wish to play:")
            while selection not in validOptions:
                selection = input("Invalid index. Select the index of the card you wish to play:")
        if selection != "":
            defence = self.hand[int(selection)]
            self.removeCard(int(selection))
            return defence
        return ""

    def promptDumpExtraCards(self, defender, inPlay, attackCount, maxAttackCount):
        selection = "-1"
        addedCards = []
        while selection != "":
            print(self.name + ", would you like to give " + defender.name + " some more cards? " +\
                "You can give them any card that would be a valid attack, up to a maximum of " +\
                str(maxAttackCount - attackCount) + " more.")
            print("Cards in play: ", inPlay+addedCards)
            print("Select a card to give " + defender.name + " that card, or just press enter to stop attacking.")
            print(self.hand)
            selection = input("Select the index of the card you wish to play:")
            validOptions = list(map(lambda x: str(x),range(len(self.hand)))) + [""] #creates a list of all possible indeces as strings, plus the empty string
            while selection not in validOptions:
                selection = input("Invalid index. Select the index of the card you wish to play:")
            while selection != "" and not DurakRulesHelperFunctions.validAttack(self.hand[int(selection)], attackCount, maxAttackCount, inPlay):
                #keeps prompting until a valid attack is given, or the aassistant chooses not to assist
                print(self.hand[int(selection)] + " is not a valid attack. Followup" +\
                      " attacks must be of the same value as a card that is already in play, "+\
                      "and total number of attacks must not exceed " + str(maxAttackCount) + ".")
                print("Cards in play: ", inPlay)
                selection = input("Select the index of the card you wish to play:")
                while selection not in validOptions:
                    selection = input("Invalid index. Select the index of the card you wish to play:")
            if selection != "":
                addedCards.append(self.hand[int(selection)])
                attackCount += 1
                self.removeCard(int(selection))
        return addedCards

