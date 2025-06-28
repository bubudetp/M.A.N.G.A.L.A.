import copy
import math

class KazanMasterAI:
    def __init__(self, max_depth=10):
        self.max_depth = max_depth
        self.transposition_table = {}

    def evaluate(self, game):
        p0_score = game.board[6]
        p1_score = game.board[13]
        p0_pits = game.get_player_pits(0)
        p1_pits = game.get_player_pits(1)

        def pit_score(pits):
            return sum(game.board[i] for i in pits)

        def good_pits(pits):
            return sum(1 for i in pits if game.board[i] > 1)

        kazan_diff = p0_score - p1_score
        pit_diff = pit_score(p0_pits) - pit_score(p1_pits)
        mobility = good_pits(p0_pits) - good_pits(p1_pits)

        score = (
            kazan_diff * 2 +
            pit_diff * 0.5 +
            mobility * 0.2
        )

        return score if game.current_player == 0 else -score

    def move_heuristic(self, game, move):
        """Encourage captures or large pits to be played first."""
        pit_index = move
        stones = game.board[pit_index]
        opponent_idx = 12 - pit_index
        opponent_stones = game.board[opponent_idx]
        score = stones

        # Prefer capture-eligible moves
        if game.can_capture_equal(pit_index):
            score += 10

        # Prefer moves with more stones
        if stones > 3:
            score += 2

        return score

    def minimax(self, game, depth, alpha, beta, maximizing):
        # Memoization key
        board_key = (tuple(game.board), game.current_player, depth)
        if board_key in self.transposition_table:
            return self.transposition_table[board_key], None

        if depth <= 0 or game.is_game_over():
            val = self.evaluate(game)
            self.transposition_table[board_key] = val
            return val, None

        legal_moves = game.legal_moves()
        if not legal_moves:
            val = self.evaluate(game)
            self.transposition_table[board_key] = val
            return val, None

        best_move = None

        # Order moves
        ordered_moves = sorted(
            legal_moves,
            key=lambda m: self.move_heuristic(game, m),
            reverse=maximizing
        )

        if maximizing:
            max_eval = -math.inf
            for move in ordered_moves:
                next_game = game.clone()
                prev_player = next_game.current_player
                next_game.make_move(move)

                next_depth = depth
                if next_game.current_player != prev_player:
                    next_depth -= 1  # Only reduce depth when turn passes

                eval, _ = self.minimax(
                    next_game,
                    next_depth,
                    alpha,
                    beta,
                    next_game.current_player == game.current_player
                )
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break

            self.transposition_table[board_key] = max_eval
            return max_eval, best_move

        else:
            min_eval = math.inf
            for move in ordered_moves:
                next_game = game.clone()
                prev_player = next_game.current_player
                next_game.make_move(move)

                next_depth = depth
                if next_game.current_player != prev_player:
                    next_depth -= 1

                eval, _ = self.minimax(
                    next_game,
                    next_depth,
                    alpha,
                    beta,
                    next_game.current_player == game.current_player
                )
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break

            self.transposition_table[board_key] = min_eval
            return min_eval, best_move

    def get_best_move(self, game):
        self.transposition_table = {}  # Reset cache each top-level call
        _, move = self.minimax(game, self.max_depth, -math.inf, math.inf, True)
        return move
