import json
import random
from code.mangala_engine import MangalaGame
from ai.kazanmaster_ai import KazanMasterAI
from code.ml.feature_extraction import extract_features

NUM_GAMES = 5000
OUTPUT_PATH = "data/training_data.json"

ai = KazanMasterAI(max_depth=6)
data = []

for _ in range(NUM_GAMES):
    game = MangalaGame()
    while not game.is_game_over():
        board_snapshot = game.clone()
        best_move = ai.get_best_move(board_snapshot)

        features = extract_features(board_snapshot)
        data.append({
            "features": features,
            "label": best_move
        })

        try:
            game.make_move(best_move)
        except:
            break

    game.end_game()

with open(OUTPUT_PATH, "w") as f:
    json.dump(data, f, indent=2)

print(f"Saved {len(data)} samples to {OUTPUT_PATH}")
