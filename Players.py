import random

class Players:
    """
    PlayersClass
    """
    __players = []
    __num_players = 4
    __partnerships = {}

    def __init__(self, num_players = 4):
        """
        Initialize Players
        """
        self.__num_players = num_players

    def setup(self):
        """
        Set Player names
        """
        # for i in range(self.__num_players):
        #     name = input(f"Enter the name of Player {i+1}: ")
        #     self.__players.append(name)
        self.__players.append("Obi")
        self.__players.append("Atiku")
        self.__players.append("Tinubu")
        self.__players.append("Kwankwaso")
    
    @property
    def players(self):
        """
        Players
        """
        return self.__players
    
    @players.setter
    def players(self):
        """
        Set player names
        """
        pass

    def set_partnerships(self):
        """
        Set up player partnerships
        """
        # self.__partnerships = {self.__players[0]: self.__players[2],
        #                 self.__players[1]: self.__players[3]}
        index = [0, 1, 2, 3]
        random.shuffle(index)
        self.__partnerships = {self.__players[index[0]]: self.__players[index[1]],
                        self.__players[index[2]]: self.__players[index[3]]}
    
    @property
    def partnerships(self):
        """
        Partnerships
        """
        return self.__partnerships
    
    @partnerships.setter
    def partnerships(self):
        """
        Set up partnerships
        """
        pass

    def initialize_scoreboard(self):
        """
        Initialize the scoreboard
        """
        scoreboard = [[0, 0] for _ in range(len(self.players))]
        return scoreboard
    
    def can_update_score(self, scoreboard, player_id, last_card = False):
        """
        Checks if the player can have scores updated
        """
        if scoreboard[player_id][1] < 3 or last_card == True:
            return True
        
        return False
    
    def update_scoreboard(self, scoreboard = [], player_id = 0, points = 0):
        """
        Updates the ScoreBoard
        """
        # if self.can_update_score(scoreboard, player_id):
        scoreboard[player_id][0] = scoreboard[player_id][0] + points
        scoreboard[player_id][1] = scoreboard[player_id][1] + 1
    
    def reset_scoreboard_tricks(self, scoreboard = []):
        """
        Resets the tricks on scoreboard
        """
        # for player in scoreboard:
        #     for score in player:
        #         score[1] = 0
        scoreboard[0][1] = 0
        scoreboard[1][1] = 0
        scoreboard[2][1] = 0
        scoreboard[3][1] = 0

    def transfer_win(self, scoreboard = [], to = 0, points = 0):
        """
        Give win points to another user
        """        
        self.update_scoreboard(scoreboard, to, points)

    def keep_card(self, cards_played = [], hands2 = []):
        """
        During last card, each player keeps the cards they played
        """
        for each in cards_played:
            for player, card in each.items():
                i = self.players.index(player)
                hands2[i].append(card)
        return hands2
    
    def exchange_cards(self, cards_played = [], hands2 = []):
        """
        Exchanges the max card with min card
        """
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Players, cls).__new__(cls)
        return cls.instance

