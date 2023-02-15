from Cards import Cards
from Players import Players

cards = Cards()
cards.shuffle()

hands = []
hand = []
min_val = 30
dealer = ""
dealer_index = 0
current_player_index = 0
next_player_index = 0

players = Players()
players.setup()
players.set_partnerships()
scoreboard = players.initialize_scoreboard()

# deal first hands and obtain first dealer
for player in range(len(players.players)):
    card = cards.deal(hand)
    hands.append(hand)
    hand = []
    if min_val > cards.get_card_value(card[0]):
        min_val = cards.get_card_value(card[0])
        dealer = players.players[player]
        dealer_index = player

current_player_index = dealer_index
next_player_index = (current_player_index + 1) % len(players.players)

# print partnerships
for player, partner in players.partnerships.items():
    print(f"\n{player} & {partner}")

# Display the preliminary round cards
for i in range(len(players.players)):
    print(f"\n{players.players[i]}: {hands[i]}")

# Display the dealer
print(f"\nDealer: {dealer}")

# Display second player
# print(f"\nSecond player: {players.players[next_player_index]}")

# Deal the rest of the cards
i = 0
while len(cards.deck) > 0:
    card = cards.deal(hands[i])
    i = (i + 1) % len(players.players)
    if min_val > cards.get_card_value(card[0]):
        min_val = cards.get_card_value(card[0])

# Display the cards for each player
for i in range(len(players.players)):
    print(f"\n{players.players[i]}: {hands[i]}")

# This tracks the number of plays in one trick which is usually 4 plays
hands_per_trick = 0
tricks = 0

max_card = 0
min_card = 32

# Game Play
while len(hands[current_player_index]) > 0:
    # print the current player and their hand
    i = current_player_index
    current_player = players.players[i]
    current_suit = None
    has_suit = False
    cards_played = []

    print(f"\n{current_player}'s turn: ")
    print(f"\n{current_player}'s hand: {hands[i]}")

    # allow the player to select a card from their hand
    play_card = None
    play_card_index = None

    while play_card is None:
        play_card_index = int(input(f"\n{current_player}, select a card to play by index (e.g.'0'): "))

        if play_card_index not in range(len(hands[i])):
            print(f"\n{current_player}, invalid card selected. Try again.")
            play_card_index = None
            continue
        
        # The card that current player selected to play
        play_card = hands[i][play_card_index]
    
        if current_suit is not None and play_card[1] != current_suit:
            for card in hands[i]:
                if card[1] == current_suit:
                    has_suit = True
        
        if has_suit:
            print(f"\n{current_player}, you must follow suit.")
            play_card = None
            continue
        
        # Tracks the cards played to get the highest and lowest values
        if max_card < cards.get_card_value(play_card[0]):
            max_card = cards.get_card_value(play_card[0])
            trick_winner = current_player_index
        if min_card > cards.get_card_value(play_card[0]):
            min_card = cards.get_card_value(play_card[0])
        
    if hands_per_trick == 3:
        transfer = input(f"\n{players.players[trick_winner]} would you like to transfer tricks to another player?\nEnter 'y' for yes or just press enter to skip: ")
        if transfer == 'y' or transfer == 'Y':
            players.transfer_win(scoreboard, min_card)
        else:
            players.update_scoreboard(scoreboard, trick_winner, min_card)
        min_card = 32
        max_card = 0
        print(f"\n{scoreboard}")
        
    hands_per_trick = (hands_per_trick + 1) % len(players.players)

    # Remove the selected card from the player's hand
    # and add the selected card to the list of cards that have been played
    cards_played.append(hands[i].pop(play_card_index))

    # print the selected card
    print(f"\n{current_player} plays: {play_card}")

    # update the current suit
    if hands_per_trick == 0:
        current_suit = play_card[1]

    # update the current player index
    current_player_index = (current_player_index + 1) % len(players.players)

    # determine the winner
    winner = None
