class MangalaGame:
    def __init__(self):
        # 0–5: P0 pits | 6: P0 kazan | 7–12: P1 pits | 13: P1 kazan
        self.board = [3] * 6 + [0] + [3] * 6 + [0]
        self.current_player = 0  # 0 = P0, 1 = P1

    def get_player_pits(self, player):
        return range(0, 6) if player == 0 else range(7, 13)

    def get_kazan_index(self, player):
        return 6 if player == 0 else 13

    def is_own_pit(self, index, player):
        return index in self.get_player_pits(player)

    def make_move(self, pit_index):
        if not self.is_own_pit(pit_index, self.current_player):
            raise ValueError("Not your pit.")
        if self.board[pit_index] <= 1:
            raise ValueError("Pit must have at least 2 stones to make a move.")

        index = pit_index
        stones = self.board[index] - 1  # Take all stones except one
        self.board[index] = 1  # Leave one stone in the pit

        while True:
            # Sow stones
            while stones > 0:
                index = (index + 1) % 14
                if self.current_player == 0 and index == 13:
                    continue  # skip opponent's kazan
                if self.current_player == 1 and index == 6:
                    continue
                self.board[index] += 1
                stones -= 1

            # Rule 1: landed in your kazan → extra turn
            if index == self.get_kazan_index(self.current_player):
                print("Last stone landed in your kazan. You go again.")
                return

            # Rule 2: your pit matches opposite → extra turn
            if self.is_own_pit(index, self.current_player):
                opposite_index = 12 - index
                if self.board[index] == self.board[opposite_index]:
                    print(f"Symmetrical stone count with pit {opposite_index}. You go again.")
                    return

            # Rule 3: relay sowing from own pit with even stones
            if self.is_own_pit(index, self.current_player) and self.board[index] >= 2 and self.board[index] % 2 == 0:
                stones = self.board[index]
                self.board[index] = 0
                print(f"Relay move from pit {index} with {stones} stones.")
                continue  # restart sowing with picked-up stones

            # Rule 4: capture if ends on 1 or 3 in own pit
            if self.is_own_pit(index, self.current_player) and self.board[index] in [1, 3]:
                kazan = self.get_kazan_index(self.current_player)
                print(f"Captured {self.board[index]} stones from pit {index}.")
                self.board[kazan] += self.board[index]
                self.board[index] = 0

            break 

        self.current_player = 1 - self.current_player


    def legal_moves(self):
        return [i for i in self.get_player_pits(self.current_player) if self.board[i] > 1]

    def is_game_over(self):
        side_0_empty = all(self.board[i] == 0 for i in range(0, 6))
        side_1_empty = all(self.board[i] == 0 for i in range(7, 13))
        return side_0_empty or side_1_empty

    def end_game(self):
        if not self.is_game_over():
            return
        for i in range(0, 6):
            self.board[6] += self.board[i]
            self.board[i] = 0
        for i in range(7, 13):
            self.board[13] += self.board[i]
            self.board[i] = 0

    def print_board(self):
        print("\nBoard:")
        print("   ", "  ".join(f"{self.board[i]:2}" for i in range(12, 6, -1)))  # Player 1 pits
        print(f"{self.board[13]:2} {' ' * 21} {self.board[6]:2}")  # Kazans
        print("   ", "  ".join(f"{self.board[i]:2}" for i in range(0, 6)))  # Player 0 pits
        print(f"\nCurrent player: {'P0' if self.current_player == 0 else 'P1'}\n")

    def print_legal_moves(self):
        print(f"Legal moves for {'P0' if self.current_player == 0 else 'P1'}:")
        for pit in self.legal_moves():
            print(f"  - Pit {pit} ({self.board[pit]} stones)")

game = MangalaGame()
game.print_board()

while not game.is_game_over():
    game.print_legal_moves()

    try:
        move = int(input("Choose a pit index: "))
        game.make_move(move)
    except Exception as e:
        print("Error:", e)
    game.print_board()

game.end_game()
game.print_board()
