from code.ai.kazanmaster_ai import KazanMasterAI

class RolloutlessKazanAI(KazanMasterAI):
    def get_best_move(self, game):
        self.transposition_table = {}
        _, move = self.minimax(game, self.max_depth, -float('inf'), float('inf'), True)
        return move
