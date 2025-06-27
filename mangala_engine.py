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
            raise ValueError("Ce n'est pas ta case.")
        if self.board[pit_index] == 0:
            raise ValueError("La case est vide.")

        opposite_index = 12 - pit_index

        if self.board[pit_index] == self.board[opposite_index] and self.board[pit_index] != 3:
            prises = self.board[pit_index] + self.board[opposite_index]
            kazan  = self.get_kazan_index(self.current_player)
            self.board[kazan] += prises
            self.board[pit_index] = 0
            self.board[opposite_index] = 0
            print(f"Capture égalité immédiate : {prises} pierres (cases {pit_index} & {opposite_index}).")
            return  # on rejoue

        if self.board[pit_index] == 1:
            raise ValueError("Il faut au moins 2 pierres pour semer (sinon capture).")

        index  = pit_index
        stones = self.board[index] - 1      # on laisse 1 pierre
        self.board[index] = 1

        while stones > 0:
            index = (index + 1) % 14
            if self.current_player == 0 and index == 13:
                continue
            if self.current_player == 1 and index == 6:
                continue
            self.board[index] += 1
            stones -= 1

        if index == self.get_kazan_index(self.current_player):
            print("Dernière pierre dans ton kazan : rejoue !")
            return

        if self.is_own_pit(index, self.current_player) and self.board[index] in (1, 3):
            kazan = self.get_kazan_index(self.current_player)
            prises = self.board[index]
            self.board[kazan] += prises
            self.board[index] = 0
            print(f"Capture 1/3 : {prises} pierre(s) prise(s) de la case {index}.")
            return 

        self.current_player = 1 - self.current_player


    def can_capture_equal(self, idx):
        """True si la case idx et sa case opposée ont le même nombre ≠ 3."""
        opp = 12 - idx
        return (self.is_own_pit(idx, self.current_player)
                and self.board[idx] == self.board[opp]
                and self.board[idx] != 3
                and self.board[idx] > 0)

    def legal_actions(self):
        """
        Renvoie une liste d’actions possibles pour le joueur courant.
        Chaque action est un tuple (idx, mode) où mode = 'C' ou 'S'.
        """
        actions = []
        for i in self.get_player_pits(self.current_player):
            if self.board[i] == 0:
                continue
            if self.can_capture_equal(i):
                actions.append((i, 'C'))
            if self.board[i] > 1:
                actions.append((i, 'S'))
        return actions


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
        P0 = {0:'A',1:'B',2:'C',3:'D',4:'E',5:'F'}
        P1 = {12:'L',11:'K',10:'J',9:'I',8:'H',7:'G'}
        labels = P0 if self.current_player == 0 else P1
        print(f"Actions possibles pour {'P0' if self.current_player==0 else 'P1'} :")
        for idx, mode in self.legal_actions():
            lab = labels[idx]
            if mode == 'C':
                print(f"  - {lab} (index {idx})  ⚔  Capture égalité ({self.board[idx]} pierres)")
            else:
                print(f"  - {lab} (index {idx})  ➜  Sème ({self.board[idx]} pierres)")


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
