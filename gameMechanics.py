import random
import json

# Starts with 100 chips, global top-level variable - score purposes
chips = 100

# The Deck class handles the deck of cards from the JSON file and contains the function
#   to draw a card from the deck JSON
class Deck:
    def __init__(self):
        with open("deckOfCards.json", "r") as file:
            self.cards_available = json.load(file)
    
    def draw_card(self):
        suits = list(self.cards_available.keys())
        suit = random.choice(suits)
        value = random.choice(self.cards_available[suit])

        self.cards_available[suit].remove(value)

        if not self.cards_available[suit]:
            del self.cards_available[suit]

        if(value != "10"):
            card = [
                "╭---------╮",
                f"| {value}       |",
                "|         |",
                f"|    {suit}    |",
                "|         |",
                f"|       {value} |",
                "╰---------╯"
            ]
        else:
            card = [
                "╭---------╮",
                f"| {value}      |",
                "|         |",
                f"|    {suit}    |",
                "|         |",
                f"|       {value}|",
                "╰---------╯"
            ]

        return card, value

# The Hand class shares common functionality for both the player and the dealer's hand. This
#   includes drawing cards from the deck, as well as determining and printing the hand (value)
class Hand:
    def __init__(self):
        self.hand = []
        self.hand_values = []
        self.hand_value = 0
    
    def draw(self, deck, n):
        i = 0
        while i < n: 
            card, value = deck.draw_card()
            self.hand.append(card)
            self.hand_values.append(value)
            i += 1
        
        self.hand_value = self.determine_hand_value()
    
    def determine_hand_value(self):
        checked_aces = False
        new_value = 0
        face_cards = ["K", "Q", "J"]

        for n in self.hand_values:
            if n in face_cards:
                new_value += 10
            elif n == "A":
                new_value += 11
            else:
                new_value += int(n)

        if(new_value > 21 and not checked_aces):
            for n in self.hand_values:
                if n == "A" and new_value > 21:
                    new_value -= 10
            checked_aces = True
        
        return new_value
        
    def print_hand(self):
        for i in range(7):
            for card in self.hand:
                print(card[i], end="  ")
            print()

# The Dealer_Hand class is a child of the Hand class with some added hole card mechanics to add
#   some level of strategy to the game
class Dealer_Hand(Hand):
    def __init__(self):
        self.hand = []
        self.hand_values = []
        self.hand_value = 0
        self.card_in_the_hole = []
        self.is_card_in_the_hole = True
        self.hole_card_checker = False
        self.hole_card = [
            "╭---------╮",
            "| \\ \\ \\ \\ |",
            "| \\ \\ \\ \\ |",
            "| \\ \\ \\ \\ |",
            "| \\ \\ \\ \\ |",
            "| \\ \\ \\ \\ |",
            "╰---------╯"
        ]

    def draw(self, deck, n):
        i = 0
        while i < n: 
            card, value = deck.draw_card()
            if(self.is_card_in_the_hole):
                self.hand.append(self.hole_card)
                self.card_in_the_hole = card
                self.is_card_in_the_hole = False
                self.hole_card_checker = True
            else:
                self.hand.append(card)
            self.hand_values.append(value)
            i += 1
        
        self.hand_value = self.determine_hand_value()

    def reveal_hole_card(self):
        self.hand[0] = self.card_in_the_hole
        self.hole_card_checker = False
        self.hand.append(self.card_in_the_hole)

# Initilaize game starts the game by generating both hands, the deck, drawing 2 cards for each
#   and printing both, this keeps the turns running until busting
# Busting just means either actually busting or the game being over due to score or stand
def initialize_game():
    busted = False
    
    print(f"\nCurrently, you have {chips} chips.")
    bet_amount = int(input(f"How much would you like to bet (1-{chips})? "))

    deck = Deck()
    player_hand = Hand()
    dealer_hand = Dealer_Hand()

    dealer_hand.draw(deck, 2)
    player_hand.draw(deck, 2)
    print_hands(dealer_hand, player_hand)

    while not busted:
        busted = turn(dealer_hand, player_hand, deck, bet_amount)
    
    if(chips <= 0):
        return False
    return True

# Each turn, the player can hit or stand, hitting draws a card and standing causes dealer to reveal
#   and then subsequently draw cards until they reach 17 where they'll stand
# If, at any time, the player hits blackjack or busts, the turn will return false and automatically
#   end the game
def turn(dealer, player, deck, bet):
    if(player.hand_value >= 21 or dealer.hand_value >= 21):
        dealer.reveal_hole_card()
        return determine_outcome(dealer, player, bet)

    action = input("Would you like to 'hit', 'stand', or 'double down'? -> ").lower()

    if(action == "hit"):
        player.draw(deck, 1)
        print_hands(dealer, player)
    elif(action == "stand"):
        dealer.reveal_hole_card()
        while dealer.hand_value < 17:
            dealer.draw(deck, 1)
        print_hands(dealer, player)
        return determine_outcome(dealer, player, bet)
    elif(action == "double down"):
        player.draw(deck, 1)
        bet *= 2
        dealer.reveal_hole_card()
        while dealer.hand_value < 17:
            dealer.draw(deck, 1)
        print_hands(dealer, player)
        return determine_outcome(dealer, player, bet)
    else:
        print(f"Invalid command: '{action}'")
        turn(dealer, player, deck)

    return False

# A list of outcomes for each game that are posible with their respective print statements
def determine_outcome(dealer, player, bet):
    global chips
    if(player.hand_value > 21):
        print(f"You busted, you lose {bet} chips!")
        chips -= bet
    elif(dealer.hand_value > 21):
        print(f"Dealer busted, you win {bet} chips!")
        chips += bet
    elif(player.hand_value == dealer.hand_value):
        print("It's a draw, all chips returned to owners!")
    elif(player.hand_value == 21):
        print(f"You hit blackjack, you win {bet} chips!")
        chips += int(bet * 1.5)
    elif(dealer.hand_value == 21):
        print(f"Dealer hits blackjack, you lose {bet} chips!")
        chips -= bet
    elif(player.hand_value > dealer.hand_value):
        print(f"You win {bet} chips!")
        chips += bet
    elif(dealer.hand_value > player.hand_value):
        print(f"Dealer wins, you lose {bet} chips!")
        chips -= bet
    else:
        print("The outcome was determined prematurely, whoops! Keep playing!")
        return False

    print()
    return True

# Runs through and prints both hands at once, since this was a recurring set of commands
#   it was put into it's own function here
def print_hands(dealer, player):
    print("\n")
    if(dealer.hole_card_checker == True):
        print(f"== DEALER'S HAND, VALUE: ? ==")
        dealer.print_hand()
    else:
        print(f"== DEALER'S HAND, VALUE: {dealer.hand_value} ==")
        dealer.print_hand()
    print(f"== PLAYER'S HAND, VALUE: {player.hand_value} ==")
    player.print_hand()