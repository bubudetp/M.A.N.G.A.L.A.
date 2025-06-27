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

    def make_move(self, pit_index):
        if not self.is_own_pit(pit_index, self.current_player):
            raise ValueError("this is not your pit")
        if self.board[pit_index] == 0:
            raise ValueError("Invalid pit no stones to play")

        stones = self.board[pit_index]
        self.board[pit_index] = 0
        index = pit_index

        while stones > 0:
            index = (index + 1) % 14
            
            if self.current_player == 0 and index == 13:
                continue
            if self.current_player == 1 and index == 6:
                continue
        
            self.board[index] += 1
            stones -= 1
        
        if self.is_own_pit(index, self.current_player) and self.board[index] == 1:
            opposite_index = 12 - index
            if self.board[opposite_index] > 0:
                kazan = self.get_kazan_index(self.current_player)
                self.board[kazan] += 1 + self.board[opposite_index]
                self.board[index] = 0
                self.board[opposite_index] = 0
        
        if index != self.get_kazan_index(self.current_player):
            self.current_player = 1 - self.current_player
        

    def legal_moves(self):
        return [i for i in self.get_player_pits(self.current_player) if self.board[i] > 0]
    
    def is_game_over(self):
        side_0_empty = all(self.board[i] == 0 for i in range(0, 6))
        side_1_empty = all(self.board[i] == 0 for i in range(7, 13))
        return side_0_empty or side_1_empty

    def end_game(self):
        if not self.is_game_over():
            return
    
        for i in range(0, 6):
            self.board[6] += self.board[i]
            self.board[i] -= 0
        
        for i in range(7, 13):
            self.board[13] += self.board[i]
            self.board[i] -= 0
        
    
    def print_board(self):
        print(f"Player 1 side (pits 12 → 7): {self.board[12:6:-1]}")
        print(f"Kazan P1: {self.board[13]} | Kazan P0: {self.board[6]}")
        print(f"Player 0 side (pits 0 → 5): {self.board[0:6]}")
        print(f"Current player: {self.current_player}")
