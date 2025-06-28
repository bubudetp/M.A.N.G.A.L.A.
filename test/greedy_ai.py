class GreedyAI:
    def get_best_move(self, game):
        return max(game.legal_moves(), key=lambda m: game.board[m])
