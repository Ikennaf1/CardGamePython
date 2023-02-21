import random

class Cards:
    """
    The card
    """

    __suits = ["Spades", "Hearts", "Diamonds", "Clubs"]
    __ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack",
                "Queen", "King", "Ace"]
    __values = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
                "10": 10, "Jack": 15, "Queen": 20, "King": 25, "Ace": 30}
    __deck = []
    
    def __init__(self):
        """
        Comment here
        """
        self.__deck = [(rank, suit) for suit in self.__suits for rank in self.__ranks]
    
    @property
    def deck(self):
        """
        Deck of cards
        """
        return self.__deck
    
    @deck.setter
    def deck():
        """
        Deck of cards
        """
        pass

    def shuffle(self):
        """
        Shuffle the deck
        """
        random.shuffle(self.__deck)
    
    def deal(self, hands):
        """
        Deal hands
        """
        card = self.__deck.pop(0)
        hands.append(card)
        return card
    
    def hands2_init(self, hands2):
        """
        Initialize hands 2
        """
        for i in range(4):
            hands2[i].append([])
        return hands2
    
    def update_hands2(self, hands2, winner_index, cards_played = []):
        """
        Updates the next round hands of trick winner with the cards played
        """
        for cards in cards_played:
            for player, card in cards.items():
                hands2[winner_index].append(card)
        return hands2
    
    def get_card_value(self, card_number):
        """
        Gets the card value based on the card number
        """
        return self.__values[card_number]
    
    def print_cards_pretty(self, cards = []):
        """
        Prints cards in human readable way
        """
        x = 0
        endline = ""
        for j, card in enumerate(cards):
            print(f"{j}: {card}\t", end=endline)
            x = (x + 1) % 4
            endline = "\n" if x == 3 else ""
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Cards, cls).__new__(cls)
        return cls.instance
