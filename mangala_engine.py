class MangalaGame:

    def __init__(self):
        # 0 - 5 -> Player 1's pits
        # 6 -> Player 1's store
        # 7 - 12 -> Player 2's pits
        # 13 -> Player 2's store
        self.board = [4] * 6 + [0] + [4] * 6 + [0]
        self.current_player = 0 # 0 or 1

    
    def get_player_pits(self, player):
        return range(0, 6) if player == 0 else range(7, 13)
    
    def get_kazan_index(self, player):
        return 6 if player == 0 else 13

    def is_own_pit(self, index, player):
        return index in self.get_player_pits(player)
