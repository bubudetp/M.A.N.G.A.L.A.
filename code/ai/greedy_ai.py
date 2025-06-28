# code/ai/greedy_ai.py

class GreedyAI:
    def __init__(self):
        pass

    def move_heuristic(self, game, move):
        stones = game.board[move]
        landing_index = (move + stones) % 14
        score = 0

        # Favor replay
        if landing_index == game.get_kazan_index(game.current_player):
            score += 5

        # Favor captures
        if game.can_capture_equal(move):
            score += 10

        # Favor high stone count
        score += stones * 0.1

        return score

    def get_best_move(self, game):
        legal = game.legal_moves()
        if not legal:
            return None
        return max(legal, key=lambda m: self.move_heuristic(game, m))
