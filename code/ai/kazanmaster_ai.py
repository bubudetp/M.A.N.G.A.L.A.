import copy
import math
import random

from code.mangala_engine import MangalaGame

class KazanMasterAI:
    def __init__(self, max_depth=10):
        self.max_depth = max_depth
        self.transposition_table = {}

    def evaluate(self, game: MangalaGame) -> float:
        p0_score = game.board[6]
        p1_score = game.board[13]
        p0_pits = game.get_player_pits(0)
        p1_pits = game.get_player_pits(1)

        def pit_score(pits):
            return sum(game.board[i] for i in pits)

        def good_pits(pits):
            return sum(1 for i in pits if game.board[i] > 1)

        # --- Baseline Metrics ---
        kazan_diff = p0_score - p1_score
        pit_diff = pit_score(p0_pits) - pit_score(p1_pits)
        mobility = good_pits(p0_pits) - good_pits(p1_pits)

        score = (
            kazan_diff * 2 +
            pit_diff * 0.5 +
            mobility * 0.2
        )

        # --- Replay Opportunities ---
        for i in game.get_player_pits(game.current_player):
            stones = game.board[i]
            if stones == 0:
                continue
            landing_index = (i + stones) % 14
            if landing_index == game.get_kazan_index(game.current_player):
                score += 3  # Reward replay possibilities

        # --- Opponent Equal-Capture Risk (1-move lookahead) ---
        risk_penalty = 0
        for i in game.get_player_pits(1 - game.current_player):
            opp = 12 - i
            if game.board[i] > 0 and game.board[i] == game.board[opp] and game.board[i] != 3:
                risk_penalty += 1
        score -= risk_penalty * 3

        # --- Opponent Mobility / Zugzwang Pressure ---
        clone = game.clone()
        clone.current_player = 1 - game.current_player
        opp_moves = len(clone.legal_moves())
        if opp_moves <= 2:
            score += 2  # Apply pressure if opponent has limited moves

        return score if game.current_player == 0 else -score

    def move_heuristic(self, game: MangalaGame, move: int) -> int:
        """Encourage captures, replays, and large pits."""
        pit_index = move
        stones = game.board[pit_index]
        opponent_idx = 12 - pit_index
        opponent_stones = game.board[opponent_idx]

        score = 0

        # Capture opportunity
        if game.can_capture_equal(pit_index):
            score += 10

        # Large pit: more options
        if stones >= 4:
            score += 2

        # Replay opportunity
        landing_index = (pit_index + stones) % 14
        if landing_index == game.get_kazan_index(game.current_player):
            score += 5

        return score

    def minimax(self, game: MangalaGame, depth: int, alpha: float, beta: float, maximizing: bool) -> tuple[float, int | None]:
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
                retained_turn = next_game.make_move(move)

                next_depth = depth
                if not retained_turn:
                    opp_legal_count = len(next_game.legal_moves())
                    if opp_legal_count > 1:
                        next_depth -= 1

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
                retained_turn = next_game.make_move(move)

                next_depth = depth
                if not retained_turn:
                    opp_legal_count = len(next_game.legal_moves())
                    if opp_legal_count > 1:
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

    def get_best_move(self, game: MangalaGame) -> int:
        self.transposition_table = {}
        _, best_move = self.minimax(game, self.max_depth, -math.inf, math.inf, True)

        # Find all moves with the same top evaluation
        legal_moves = game.legal_moves()
        scores = []
        best_score = -math.inf
        best_moves = []

        for move in legal_moves:
            sim_game = game.clone()
            sim_game.make_move(move)
            val, _ = self.minimax(
                sim_game,
                self.max_depth - 1,
                -math.inf,
                math.inf,
                sim_game.current_player == game.current_player
            )
            if val > best_score:
                best_score = val
                best_moves = [move]
            elif val == best_score:
                best_moves.append(move)

        if len(best_moves) == 1:
            return best_moves[0]

        rollout_scores = [
            (move, self.simulate_rollouts(game, move, num_simulations=5, loss_cutoff=-15))
            for move in best_moves
        ]
        rollout_scores.sort(key=lambda x: x[1], reverse=True)
        return rollout_scores[0][0]

    def simulate_rollouts(self, game: MangalaGame, move: int, num_simulations: int = 5, loss_cutoff: int= -15) -> float:
        total_score = 0
        valid_simulations = 0

        for _ in range(num_simulations):
            sim_game = game.clone()
            sim_game.make_move(move)

            # Play until end using greedy policy
            while not sim_game.is_game_over():
                legal = sim_game.legal_moves()
                if not legal:
                    break

                # Greedy move: pick the one with highest immediate heuristic
                best = max(legal, key=lambda m: self.move_heuristic(sim_game, m))
                sim_game.make_move(best)

            sim_game.end_game()
            p0_score = sim_game.board[6]
            p1_score = sim_game.board[13]
            result = p0_score - p1_score
            signed_result = result if game.current_player == 0 else -result

            # Cutoff: ignore simulations that result in major loss
            if signed_result < loss_cutoff:
                continue

            total_score += signed_result
            valid_simulations += 1

        if valid_simulations == 0:
            return -float('inf')  # Penalize unsafe move
        return total_score / valid_simulations
