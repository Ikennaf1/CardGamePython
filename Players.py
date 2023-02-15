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
        self.__partnerships = {self.__players[0]: self.__players[2],
                        self.__players[1]: self.__players[3]}
    
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
    
    def update_scoreboard(self, scoreboard = [], player_id = 0, points = 0):
        """
        Updates the ScoreBoard
        """
        scoreboard[player_id][0] = scoreboard[player_id][0] + points
        scoreboard[player_id][1] = scoreboard[player_id][1] + 1

    def transfer_win(self, _from = 0, _to = 0):
        """
        Give win points to another user
        """
        pass

