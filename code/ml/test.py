# Warm-up: simulate one full game to estimate average duration
import time
import json
import random
from code.mangala_engine import MangalaGame
from ai.kazanmaster_ai import KazanMasterAI
from code.ml.feature_extraction import extract_features

print("Estimating time per game...")
ai = KazanMasterAI(max_depth=3)
warmup_game = MangalaGame()
start = time.time()
while not warmup_game.is_game_over():
    move = ai.get_best_move(warmup_game)
    warmup_game.make_move(move)
warmup_game.end_game()
duration = time.time() - start
print(f"One game took ~{duration:.2f} seconds, estimated total: ~{duration * 5000 / 60:.1f} minutes")
