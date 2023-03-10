from Cards import Cards
from Players import Players

game_round = 1
quit_game = 0
round_winner = None

cards = Cards()
cards.shuffle()

hands = []
hands2 = []
hands2 = cards.hands2_init(hands2)
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
print("\nPlayer Partnerships:")
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
    if game_round == 1:
        print("\nPreliminary Round\n")
    else:
        # quit_game = 0
        # round_winner = None
        hands = hands2.copy()
        hands2 = cards.hands2_init(hands2)
        # players.set_partnerships()
        # # print partnerships
        # print("\nPlayer Partnerships:")
        # for player, partner in players.partnerships.items():
        #     print(f"\n{player} & {partner}")
        players.reset_scoreboard_tricks(scoreboard)

        print(f"\nROUND {game_round}\n")

    cards_played = []
    tricks = 0
    suit_followed = True

    # deal first hands and obtain first dealer
    if game_round == 1:
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
        next_player = players.players[next_player_index]

    # Display preliminary hands
    if game_round == 1:
        for i in range(len(players.players)):
            print(f"\n{players.players[i]}: {hands[i]}")

    if game_round > 1 and round_winner is not None:
        current_player_index = round_winner
        dealer = players.players[round_winner]
        round_winner = None
    
    # Display dealer
    print(f"\nDealer: {dealer}")
    print(f"\nPlayer to the left: {next_player}")

    i = 0
    while len(cards.deck) > 0:
        card = cards.deal(hands[i])
        i = (i + 1) % len(players.players)
        if min_val > cards.get_card_value(card[0]):
            min_val = cards.get_card_value(card[0])

    # Display the cards for each player
    print("\nUpdated Hands:")
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
                if has_suit == False:
                    current_suit = None
                    suit_followed = False
            
            if has_suit:
                print(f"\n{current_player}, you must follow suit.")
                play_card = None
                play_card_index = None
                has_suit = False
                continue

            if current_suit is None and hands_per_trick == 0:
                current_suit = play_card[1]
            
            # Tracks the cards played to get the highest and lowest values
            if max_card < cards.get_card_value(play_card[0]):
                max_card = cards.get_card_value(play_card[0])
                trick_winner = current_player_index
            if min_card > cards.get_card_value(play_card[0]):
                min_card = cards.get_card_value(play_card[0])
            
        if hands_per_trick == 3:
            current_suit = None
            has_suit = False
            # Remove the selected card from the player's hand
            #   and add the selected card to the list of cards that have been played
            card_played = {}
            card_played[current_player] = hands[i].pop(play_card_index)
            cards_played.append(card_played)

            # Print cards played
            print("\nCards Played:")
            for each in cards_played:
                for played, card in each.items():
                    played = played.ljust(15)
                    print(f"{played}:{card}")
            
            # If suits not followed, determine winner
            if suit_followed == False:
                if len(hands[current_player_index]) > 0:
                    suit_followed = True
                max_trick_score = 0
                first_suit = tuple(cards_played[0].values())
                # print(first_suit)
                for each in cards_played:
                    by_line = True
                    for pl, crd in each.items():
                        if crd[1] != first_suit[0][1]:
                            by_line = False
                            break
                        else:
                            if cards.get_card_value(crd[0]) > max_trick_score:
                                max_trick_score = cards.get_card_value(crd[0])
                                trick_winner = players.players.index(pl)
                    if by_line == False:
                        break
            
            # List players to transfer points to
            print(f"\n{players.players[trick_winner]} wins trick {tricks + 1}!")
            transfer_tricks = input(f"\n{players.players[trick_winner]} would you like to transfer tricks to another player? (yes/no) ")
            if transfer_tricks.lower() == "yes":
                transfer = None
                while transfer not in range(len(players.players)):
                    print("\nSelect player by index: (e.g. 0)")
                    for j, player in enumerate(players.players):
                        print(f"{j} {player}")
                    transfer = int(input())
                to = transfer

                # Check if last card
                if len(hands[to]) == 0:
                    # players.update_scoreboard(scoreboard, to, min_card)
                    if suit_followed == False:
                        print("\nEvery player keeps their cards played.")
                        hands2 = players.keep_card(cards_played, hands2)
                        players.update_scoreboard(scoreboard, to, min_card)
                    else:
                        last_min_card = 32
                        last_max_card = 0
                        last_min_player = ""
                        last_max_player = ""
                        last_max_index = 0
                        last_min_index = 0
                        for lc, last_cards in enumerate(cards_played):
                            for ply, lstcrd in last_cards.items():
                                if cards.get_card_value(lstcrd[0]) > last_max_card:
                                    last_max_card = cards.get_card_value(lstcrd[0])
                                    last_max_player = ply
                                    last_max_index = lc
                                if cards.get_card_value(lstcrd[0]) < last_min_card:
                                    last_min_card = cards.get_card_value(lstcrd[0])
                                    last_min_player = ply
                                    last_min_index = lc
                        print(f"\n{last_max_player} and {last_min_player} exchange cards.")
                        cards_played[last_max_index][last_max_player], cards_played[last_min_index][last_min_player] = cards_played[last_min_index][last_min_player], cards_played[last_max_index][last_max_player]
                        hands2 = players.keep_card(cards_played, hands2)
                        players.transfer_win(scoreboard, players.players.index(last_min_player), min_card)
                    hands_per_trick = (hands_per_trick + 1) % len(players.players)
                    break

                while players.can_update_score(scoreboard, to, (len(cards_played) >= (52 - len(players.players)))) == False:
                    print(f"\n{players.players[to]} maximum tricks reached. {players.players[trick_winner]} Choose another player.")
                    transfer = None
                    while transfer not in range(len(players.players)):
                        print("\nSelect player by index: (e.g. 0)")
                        for j, player in enumerate(players.players):
                            print(f"{j} {player}")
                        transfer = int(input())
                    to = transfer
                players.update_scoreboard(scoreboard, to, min_card)
                cards.update_hands2(hands2, to, cards_played)
                trick_winner = to
            else:
                to = trick_winner

                # Check if last card
                if len(hands[to]) == 0:
                    # players.update_scoreboard(scoreboard, to, min_card)
                    if suit_followed == False:
                        print("\nEvery player keeps their cards played.")
                        hands2 = players.keep_card(cards_played, hands2)
                        players.update_scoreboard(scoreboard, to, min_card)
                    else:
                        last_min_card = 32
                        last_max_card = 0
                        last_min_player = ""
                        last_max_player = ""
                        last_max_index = 0
                        last_min_index = 0
                        for lc, last_cards in enumerate(cards_played):
                            for ply, lstcrd in last_cards.items():
                                if cards.get_card_value(lstcrd[0]) > last_max_card:
                                    last_max_card = cards.get_card_value(lstcrd[0])
                                    last_max_player = ply
                                    last_max_index = lc
                                if cards.get_card_value(lstcrd[0]) < last_min_card:
                                    last_min_card = cards.get_card_value(lstcrd[0])
                                    last_min_player = ply
                                    last_min_index = lc
                        print(f"\n{last_max_player} and {last_min_player} exchange cards.")
                        cards_played[last_max_index][last_max_player], cards_played[last_min_index][last_min_player] = cards_played[last_min_index][last_min_player], cards_played[last_max_index][last_max_player]
                        hands2 = players.keep_card(cards_played, hands2)
                        players.transfer_win(scoreboard, players.players.index(last_min_player), min_card)
                    hands_per_trick = (hands_per_trick + 1) % len(players.players)
                    break
                
                while players.can_update_score(scoreboard, to, (len(cards_played) >= (52 - len(players.players)))) == False:
                    print(f"\n{players.players[to]} maximum tricks reached. {players.players[trick_winner]} Choose another player.")
                    transfer = None
                    while transfer not in range(len(players.players)):
                        print("\nSelect player by index: ")
                        for j, player in enumerate(players.players):
                            print(f"{j} {player}")
                        transfer = int(input())
                    to = transfer
                players.transfer_win(scoreboard, to, min_card)
                cards.update_hands2(hands2, to, cards_played)
                trick_winner = to
            print(f"\n{players.players[trick_winner]} is awarded {min_card} points")
            
            print("\nCurrent Score:")
            for j, score in enumerate(scoreboard):
                the_player = players.players[j].ljust(15)
                print(f"{j}. {the_player}{score[0]}")
            current_player_index = trick_winner
            min_card = 32
            max_card = 0
            hands_per_trick = (hands_per_trick + 1) % len(players.players)
            tricks += 1

            # Print Updated hands
            print("\nUpdated Hands:")
            for i in range(len(players.players)):
                print(f"\n{players.players[i]}")
                cards.print_cards_pretty(hands[i])

            cards_played = []
            continue
            
        hands_per_trick = (hands_per_trick + 1) % len(players.players)

        # Remove the selected card from the player's hand
        # and add the selected card to the list of cards that have been played
        card_played = {}
        card_played[current_player] = hands[i].pop(play_card_index)
        cards_played.append(card_played)

        # print the selected card
        print(f"\n{current_player} plays: {play_card}")

        # Print cards played
        print("\nCards Played:")
        for each in cards_played:
            for played, card in each.items():
                played = played.ljust(15)
                print(f"{played}:{card}")

        # update the current suit
        if hands_per_trick == 0:
            current_suit = play_card[1]

        # update the current player index
        current_player_index = (current_player_index + 1) % len(players.players)
        # cards_played = []

    print("\nCurrent Score:")
    for j, score in enumerate(scoreboard):
        the_player = players.players[j].ljust(15)
        print(f"{j}. {the_player}{score[0]}")
    
    # determine the winner
    round_winner = 0
    for j, score in enumerate(scoreboard):
        if score[0] > score[round_winner]:
            round_winner = j
    if game_round == 1:
        print(f"\nPreliminary Round winner is: {players.players[round_winner]}")
    else:
        print(f"\nRound {game_round} winner is: {players.players[round_winner]}")
    
    check_sudden_death = False
    max_score = 0
    for score in scoreboard:
        if score[0] > max_score:
            max_score = score[0]
    if max_score >= 60:
        check_sudden_death = True
            
    if check_sudden_death is True:
        sudden_death_msg = "\nSudden death. Game Ends!!!"
        if game_round == 1 and max_score >= 60:
            print(f"\n{sudden_death_msg}")
            break
        elif game_round == 2 and max_score >= 120:
            print(f"\n{sudden_death_msg}")
            break
        elif game_round == 3 and max_score >= 180:
            print(f"\n{sudden_death_msg}")
            break
        elif game_round == 4 and max_score >= 240:
            print(f"\n{sudden_death_msg}")
            break
        else:
            print("No Sudden Death. Game can continue.\n")
    else:
        print("No Sudden Death. Game can continue.\n")

    # Quit or continue to next round
    quit_game = int(input("\n0. Continue\t1. Quit\n"))
    if quit_game == 0:
        game_round += 1
