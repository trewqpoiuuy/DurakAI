import DurakRulesHelperFunctions
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
        pass

    def promptFollowupAttack(self, defender, inPlay, attackCount, maxAttackCount):
        """Asks player to choose a followup attack, and if none is chosen, asks whether assistance is allowed. Returns None if assistance is requested"""
        pass

    def promptAssistAttack(self, attacker, defender, inPlay, attackCount, maxAttackCount):
        """Asks player to chose an assist attack"""
        pass

    def promptDefence(self, attacker, attack, trump):
        """Asks player to defend from an attack"""
        pass

    def promptDumpExtraCards(self, defender, inPlay, attackCount, maxAttackCount):
        """Prompts a player to give their extra cards to the defender after they cave conceded a bout"""
        pass

class HumanPlayer(Player):
    def __init__(self, name):
        Player.__init__(self, name)

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

class AIPlayer(Player):
    def promptFirstAttack(self, defender):
        """Asks player to chose a card to begin a bout"""
        pass

    def promptFollowupAttack(self, defender, inPlay, attackCount, maxAttackCount):
        """Asks player to choose a followup attack, and if none is chosen, asks whether assistance is allowed. Returns None if assistance is requested"""
        pass

    def promptAssistAttack(self, attacker, defender, inPlay, attackCount, maxAttackCount):
        """Asks player to chose an assist attack"""
        pass

    def promptDefence(self, attacker, attack, trump):
        """Asks player to defend from an attack"""
        for card in self.hand:
            if DurakRulesHelperFunctions.validDefence(attack, card, trump[-1]):
                return card
        return ""

    def promptDumpExtraCards(self, defender, inPlay, attackCount, maxAttackCount):
        """Prompts a player to give their extra cards to the defender after they cave conceded a bout"""
        pass
