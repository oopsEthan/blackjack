from gameMechanics import initialize_game

# Prints opening statements once, then initializes the game
print("Initializing game of Blackjack...")
print("- Dealer stands on 17\n")
game_state = initialize_game()

# After finishing the first game, prompts to play again
again = input("Play again? (y/n) -> ").lower()

# If player wants to play again, it will simply re-run the last two lines
while again == "y":
    if game_state:
        game_state = initialize_game()
    else:
        print("You've got no more money, bro. Get out of here!")
        break

    again = input("Play again? (y/n) -> ")