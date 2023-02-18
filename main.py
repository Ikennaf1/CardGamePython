from Cards import Cards
from Players import Players

game_round = 1
quit_game = 0
round_winner = None

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

# print partnerships
for player, partner in players.partnerships.items():
    print(f"\n{player} & {partner}")

# This tracks the number of plays in one trick which is usually 4 plays
hands_per_trick = 0
tricks = 0

max_card = 0
min_card = 32
current_suit = None

# Game Play
while game_round > 0 and quit_game == 0:
    print(f"\nROUND {game_round}\n")

    cards = Cards()
    cards.shuffle()
    cards_played = []

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

    # Display preliminary hands
    for i in range(len(players.players)):
        print(f"\n{players.players[i]}: {hands[i]}")

    if game_round > 1 and round_winner is not None:
        current_player_index = round_winner
        dealer = players.player[round_winner]
        round_winner = None
    
    # Display dealer
    print(f"\nDealer: {dealer}")

    i = 0
    while len(cards.deck) > 0:
        card = cards.deal(hands[i])
        i = (i + 1) % len(players.players)
        if min_val > cards.get_card_value(card[0]):
            min_val = cards.get_card_value(card[0])

    # Display the cards for each player
    for i in range(len(players.players)):
        print(f"\n{players.players[i]}")
        cards.print_cards_pretty(hands[i])

    while len(hands[current_player_index]) > 0:
        # print the current player and their hand
        i = current_player_index
        current_player = players.players[i]
        has_suit = False
        # cards_played = []

        print(f"\n{current_player}'s turn: ")
        print(f"\n{current_player}'s hand:")
        cards.print_cards_pretty(hands[i])
        

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
                play_card_index = None
                has_suit = False
                continue

            if current_suit is None:
                current_suit = play_card[1]
            
            # Tracks the cards played to get the highest and lowest values
            if max_card < cards.get_card_value(play_card[0]):
                max_card = cards.get_card_value(play_card[0])
                trick_winner = current_player_index
            if min_card > cards.get_card_value(play_card[0]):
                min_card = cards.get_card_value(play_card[0])
            
        if hands_per_trick == 3:
            j = 0
            current_suit = None
            has_suit = False
            # List players to transfer points to
            print(f"\n{players.players[trick_winner]} would you like to transfer tricks to another player?\nEnter index of player or just press enter to skip: ")
            for player in players.players:
                print(f"{j} {player}")
                j += 1
            transfer = input()
            if transfer != '':
                to = int(transfer)
                while players.can_update_score(scoreboard, to, (len(cards_played) >= (52 - len(players.players)))) == False:
                    print(f"\n{players.players[to]} maximum tricks reached. Choose another player.")
                    to = int(input())
                players.transfer_win(scoreboard, to, min_card)
                trick_winner = to
            else:
                to = trick_winner
                while players.can_update_score(scoreboard, to, (len(cards_played) >= (52 - len(players.players)))) == False:
                    # print(f"\n{len(cards_played)}\t{len(players.players)}")
                    print(f"\n{players.players[to]} maximum tricks reached. Choose another player.")
                    to = int(input())
                players.update_scoreboard(scoreboard, to, min_card)
                trick_winner = to
            print(f"\n{players.players[trick_winner]} wins with {min_card} points")
            # print(f"\nTotal points:\n\t{scoreboard}")
            print("\nCurrent Score:")
            j = 0
            for score in scoreboard:
                print(f"{j}. {players.players[j]}\t{score[0]}")
                j += 1
            current_player_index = trick_winner
            min_card = 32
            max_card = 0
            hands_per_trick = (hands_per_trick + 1) % len(players.players)
            # Remove the selected card from the player's hand
            # and add the selected card to the list of cards that have been played
            cards_played.append(hands[i].pop(play_card_index))
            continue
            
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
    j = 0
    round_winner = 0
    for score in scoreboard:
        if score[0] > round_winner:
            round_winner = j
        j += 1
    print(f"\nRound {game_round} winner is: {players.players[round_winner]}")
    
    max_score = 0
    for score in scoreboard:
        if score[0] > max_score:
            max_score = score[0]
    if max_score >= 60:
        check_sudden_death = True
            
    if check_sudden_death is True:
        sudden_death_msg = "\nSudden death"
        match game_round:
            case 1:
                if max_score >= 60:
                    print(sudden_death_msg)
                    sudden_death = True
            case 2:
                if max_score >= 120:
                    print(sudden_death_msg)
                    sudden_death = True
            case 3:
                if max_score >= 180:
                    print(sudden_death_msg)
                    sudden_death = True
            case _:
                sudden_death = False
                pass
    if sudden_death == True:
        break

    # Quit or continue to next round
    quit_game = int(input("\n0. Continue\t1. Quit\n"))
    if quit_game == 0:
        game_round += 1
