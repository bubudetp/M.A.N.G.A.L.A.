import random

class RandomAI:
    def get_best_move(self, game):
        return random.choice(game.legal_moves())
