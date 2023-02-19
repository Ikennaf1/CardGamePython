import random

# Create the deck of cards
suits = ['Spades', 'Hearts', 'Diamonds', 'Clubs']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'Jack': 15, 'Queen': 20,
          'King': 25, 'Ace': 30}
deck = [(rank, suit) for suit in suits for rank in ranks]

# Shuffle the deck
random.shuffle(deck)

# Allow players to input their names
players = []
for i in range(4):
    name = input(f"Enter the name of Player {i+1}: ")
    players.append(name)

all_points = [0, 0, 0, 0]
quit_game = 0
game_round = 0


# Create player partnerships
partnerships = {players[0]:players[2], players[1]:players[3]}

# Deal one card to each player in the preliminary round
preliminary_hands = {player: [] for player in players}
for i, player in enumerate(players):
    preliminary_hands[player].append(deck[i])

# Find the dealer based on the preliminary round
dealer = min(preliminary_hands, key=lambda x: ranks.index(preliminary_hands[x][0][0]))

# Deal the remaining cards to each player
player_hands = {player: [] for player in players}
player_trick_hand = {player: [] for player in players}
start = 0
for i in range(13):
    for j, player in enumerate(players):
        if start + j >= len(deck):
            break
        player_hands[player].append(deck[start + j])
    start += 4

def select_player(players, current_player):
  # Get the current player's index value
  current_index = players.index(current_player)

  # Return the current player's index
  return current_index

dealer_index = players.index(dealer)

# Calculate the index of the player who will play second
second_player_index = (dealer_index + 1) % len(players)
second_player = players[second_player_index]

# Display the player partnerships
print("\nPlayer Partnerships:")
for player, partner in partnerships.items():
    print(f"{player} & {partner}")

# Display the preliminary round cards
print("\nPreliminary Round:")
for player, hand in preliminary_hands.items():
    print(f"{player}: {hand}")

# Display the dealer
print(f"\nDealer: {dealer}")

# Display player left to the dealer
print(f"Player to the left: {second_player}")
print("\n")
# Display the cards for each player
for player, hand in player_hands.items():
    print(f"\n{player}:\n{hand}")


def play_game(players, dealer, player_hands, partnerships, second_player, player):

        # Keep track of the card values
        values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'Jack': 15, 'Queen': 20,
              'King': 25, 'Ace': 30}

        ########################################################################
        # fresh_round = True
        # if fresh_round == True:
        #     # Shuffle the deck
        #     random.shuffle(deck)
        #     all_points = [0, 0, 0, 0]

        #     # Deal the remaining cards to each player
        #     player_hands = {player: [] for player in players}
        #     player_trick_hand = {player: [] for player in players}
        #     start = 0
        #     for i in range(13):
        #         for j, player in enumerate(players):
        #             if start + j >= len(deck):
        #                 break
        #             player_hands[player].append(deck[start + j])
        #         start += 4
        #     fresh_round = False
        ########################################################################

        # keep track of the cards that have been played
        cards_played = []
        cards_played_with_player_names = {}
        current_player = second_player
        current_suit = None
        winner = None
        winning_card = None

        # loop through all of the players
        for i in range(len(players)):
            # check if the player has any cards left in their hand
            if not player_hands[current_player]:
                break

            # print the current player and their hand
            print(f"\n{current_player}'s turn:")
            print(f"{current_player}'s hand:")
            h = 0
            hi = 0
            endline = ""
            for hand in player_hands[current_player]:
                print(f"{hi}: {hand}\t", end=endline)
                hi += 1
                h = (h + 1) % 4
                endline = "\n" if h == 3 else ""

            # allow the player to select a card from their hand
            selected_card = None
            while selected_card is None:
                selected_card_index = int(input(f"{current_player}, select a card to play by index (e.g. '0'): "))
                if selected_card_index >= 0 and selected_card_index < len(player_hands[current_player]):
                    selected_card = player_hands[current_player][selected_card_index]

                    # check if the player must follow suit
                    if current_suit is not None and selected_card[1] != current_suit:
                        has_suit = False
                        for card in player_hands[current_player]:
                            if card[1] == current_suit:
                                has_suit = True
                                break

                        if has_suit:
                            print(f"{current_player}, you must follow suit.")
                            selected_card = None
                            continue

                if selected_card is None:
                    print(f"{current_player}, invalid card selected. Try again.")

            # remove the selected card from the player's hand
            player_hands[current_player].remove(selected_card)

            # add the selected card to the list of cards that have been played
            cards_played.append(selected_card)
            cards_played_with_player_names[current_player] = selected_card

            # print the selected card
            print(f"{current_player} plays: {selected_card}")

            # update the current suit
            current_suit = selected_card[1]

            # Check if the selected card has a higher value than the winning card
            if winning_card is None or values[selected_card[0]] > values[winning_card[0]]:
                winner = current_player
                winning_card = selected_card

            if current_suit is not None and selected_card[1] != current_suit:
                winner = players[0]
                winning_card = selected_card
                points = values[selected_card[0]]
                break

            # update the current player
            current_index = players.index(current_player)
            current_player = players[(current_index + 1) % len(players)]

            # award points to the winning player
            played_values = [values[card[0]] for card in cards_played]
            points = min(played_values)
            # Keep track of the cards played by each player
            cards_played_by_player = {}
            for player in players:
                cards_played_by_player[player] = []

            # print the final list of cards that have been played
            print(f"\nCards played:")
            for player, card in cards_played_with_player_names.items():
                print(f"\t{player}: {card}")

        # display the winner and the points awarded
        # if fresh_round == False:
        #     print(f"{winner} wins this round wins with {winning_card} and is awarded {points} points.")
        print(f"{winner} wins this round wins with {winning_card} and is awarded {points} points.")

        # print(f"Current points: {all_points}")
        # print(f"Current standing:")
        # for player in players:
        #     print(f"{player}:\t{all_points[players.index(player)]}")

        # Display the updated hand for each player
        print("\nUpdated hands for each player:")
        for player in players:
            print(f"\n{player}:\t{player_hands[player]}")

        # ask the winner if they want to keep the cards or give them to another player
        keep_cards = input(f"{winner}, do you want to keep the cards (yes/no)? ")
        if keep_cards.lower() == 'yes':
            if check_player_trick_hand(winner):
                # keep the cards
                player_trick_hand[winner] += cards_played
                # Award points to the winner
                all_points[players.index(winner)] += points
                # Display which player currently has the cards_played
                print(f"{winner} now has the cards_played.")
                current_player = winner
            else:
                recipient = None
                while recipient is None:
                    recipient_name = input(f"{winner}, select the player to give the cards to: ")
                    if recipient_name in players:
                        if check_player_trick_hand(recipient_name):
                            recipient = recipient_name
                    else:
                        print(f"{recipient_name} is not a valid player. Try again.")
                player_trick_hand[recipient] += cards_played
                # Award points to the winner
                all_points[players.index(recipient)] += points
                current_player = recipient
        else:
            # give the cards to another player
            recipient = None
            while recipient is None:
                recipient_name = input(f"{winner}, select the player to give the cards to: ")
                if recipient_name in players:
                    if check_player_trick_hand(recipient_name):
                        recipient = recipient_name
                else:
                    print(f"{recipient_name} is not a valid player. Try again.")
            player_trick_hand[recipient] += cards_played
            # Award points to the winner
            all_points[players.index(recipient)] += points
            current_player = recipient

            # Display which player currently has the cards_played
            print(f"{recipient} now has the trick.")
        print(f"Current standing:")
        for player in players:
            print(f"{player}:\t{all_points[players.index(player)]}")

        # keep track of the cards played by each player
        cards_played = {}


        for player_name, player_cards in cards_played.items():
            print(f"{player_name}: {player_cards}")


        for trick in range(12):
            # Keep track of the card values
            values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'Jack': 15, 'Queen': 20,
                      'King': 25, 'Ace': 30}

            # keep track of the cards that have been played
            cards_played = []
            cards_played_with_player_names = {}
            current_suit = None
            winner = None
            winning_card = None
            # loop through all of the players
            for i in range(len(players)):
                # check if the player has any cards left in their hand
                if not player_hands[current_player]:
                    break

                # print the current player and their hand
                print(f"\n{current_player}'s turn:")
                print(f"{current_player}'s hand:")
                # print(f"{current_player}'s hand: {player_hands[current_player]}")
                h = 0
                hi = 0
                endline = ""
                for hand in player_hands[current_player]:
                    print(f"{hi}: {hand}\t", end=endline)
                    hi += 1
                    h = (h + 1) % 4
                    endline = "\n" if h == 3 else ""

                # allow the player to select a card from their hand
                selected_card = None
                while selected_card is None:
                    selected_card_index = int(input(f"\n{current_player}, select a card to play by index (e.g. '0'): "))
                    if selected_card_index >= 0 and selected_card_index < len(player_hands[current_player]):
                        selected_card = player_hands[current_player][selected_card_index]

                        # check if the player must follow suit
                        if current_suit is not None and selected_card[1] != current_suit:
                            has_suit = False
                            for card in player_hands[current_player]:
                                if card[1] == current_suit:
                                    has_suit = True
                                    break

                            if has_suit:
                                print(f"{current_player}, you must follow suit.")
                                selected_card = None
                                continue

                    if selected_card is None:
                        print(f"{current_player}, invalid card selected. Try again.")

                # remove the selected card from the player's hand
                player_hands[current_player].remove(selected_card)

                # add the selected card to the list of cards that have been played
                cards_played.append(selected_card)
                cards_played_with_player_names[current_player] = selected_card

                # print the selected card
                print(f"{current_player} plays: {selected_card}")

                # update the current suit
                current_suit = selected_card[1]

                # Check if the selected card has a higher value than the winning card
                if winning_card is None or values[selected_card[0]] > values[winning_card[0]]:
                    winner = current_player
                    winning_card = selected_card

                if current_suit is not None and selected_card[1] != current_suit:
                    winner = players[0]
                    winning_card = selected_card
                    points = values[selected_card[0]]
                    break

                # update the current player
                current_index = players.index(current_player)
                current_player = players[(current_index + 1) % len(players)]

                # award points to the winning player
                played_values = [values[card[0]] for card in cards_played]
                points = min(played_values)
                # Keep track of the cards played by each player
                cards_played_by_player = {}
                for player in players:
                    cards_played_by_player[player] = []

                # print the final list of cards that have been played
                print(f"\nCards played:")
                for player, card in cards_played_with_player_names.items():
                    print(f"\t{player}: {card}")

            # display the winner and the points awarded
            print(f"{winner} wins this round wins with {winning_card} and is awarded {points} points.")

            # Display the updated hand for each player
            print("\nUpdated hands for each player:")
            for player in players:
                print(f"\n{player}:\t{player_hands[player]}")

            # ask the winner if they want to keep the cards or give them to another player
            keep_cards = input(f"{winner}, do you want to keep the cards (yes/no)? ")
            if keep_cards.lower() == 'yes':
                # if trick == 11:
                #     second_player = winner
                #     break
                if check_player_trick_hand(winner):
                    # keep the cards
                    player_trick_hand[winner] += cards_played
                    # Award points to the winner
                    all_points[players.index(winner)] += points
                    # Display which player currently has the cards_played
                    print(f"{winner} now has the cards_played.")
                    current_player = winner
                else:
                    recipient = None
                    while recipient is None:
                        recipient_name = input(f"{winner}, select the player to give the cards to: ")
                        if recipient_name in players:
                            # if trick == 11:
                            #     recipient = recipient_name
                            #     second_player = recipient_name
                            #     break
                            if check_player_trick_hand(recipient_name):
                                recipient = recipient_name
                        else:
                            print(f"{recipient_name} is not a valid player. Try again.")
                    player_trick_hand[recipient] += cards_played
                    # Award points to the winner
                    all_points[players.index(recipient)] += points
                    current_player = recipient
            else:
                # give the cards to another player
                recipient = None
                while recipient is None:
                    recipient_name = input(f"{winner}, select the player to give the cards to: ")
                    if recipient_name in players:
                        # if trick == 11:
                        #         recipient = recipient_name
                        #         second_player = recipient_name
                        #         break
                        if check_player_trick_hand(recipient_name):
                            recipient = recipient_name
                    else:
                        print(f"{recipient_name} is not a valid player. Try again.")
                # if trick == 11:
                #     # recipient = recipient_name
                #     second_player = recipient_name
                #     break
                player_trick_hand[recipient] += cards_played
                # Award points to the winner
                all_points[players.index(recipient)] += points
                current_player = recipient

                # Display which player currently has the cards_played
                print(f"{recipient} now has the trick.")
            print(f"Current standing:")
            for player in players:
                print(f"{player}:\t{all_points[players.index(player)]}")

            # keep track of the cards played by each player
            cards_played = {}

            for player_name, player_cards in cards_played.items():
                print(f"{player_name}: {player_cards}")
            
            # if trick == 11:
            #     break

        
        print("Playing trick", trick + 1)
        # trick = None

def check_player_trick_hand(the_player):
    if len(player_trick_hand[the_player]) < 12:
        print(player_trick_hand[the_player])
        return True
    else:
        print(f"\n{players[players.index(the_player)]} maximum tricks reached. Please choose another player.")
        return False

def check_sudden_death(the_game_round, points = []):
    max_point = max(points)
    if the_game_round == 1 and max_point >= 60:
        print("\nSudden Death!!!")
        return True
    elif the_game_round == 2 and max_point >= 120:
        print("\nSudden Death!!!")
        return True
    elif the_game_round == 3 and max_point >= 180:
        print("\nSudden Death!!!")
        return True
    elif the_game_round == 4 and max_point >= 240:
        print("\nSudden Death!!!")
        return True
    else:
        print(f"\nRound{game_round}:\tNo sudden death. Continue.")
        return False

while quit_game == 0:
    game_round += 1
    play_game(players, dealer, player_hands, partnerships, second_player, player)
    if check_sudden_death(game_round, all_points) == False:
        continue_playing = input("\nDo you wish to continue game? (yes/no) ")
        if continue_playing == "yes":
            quit_game = 0
        else:
            quit_game = 1
    else:
        quit_game = 1