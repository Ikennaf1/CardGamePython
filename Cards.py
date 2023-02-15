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
        djfnnf
        """
        return self.__deck
    
    @deck.setter
    def deck():
        """
        jdfgno
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
    
    def get_card_value(self, card_number):
        """
        Gets the card value based on the card number
        """
        return self.__values[card_number]
