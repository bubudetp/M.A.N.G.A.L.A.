import numpy as np

def extract_features(game):
    board = game.board
    current_player = game.current_player

    # Player 0 pits: 0-5, kazan: 6
    # Player 1 pits: 7-12, kazan: 13

    p0_pits = board[0:6]
    p1_pits = board[7:13]
    p0_kazan = board[6]
    p1_kazan = board[13]

    # Basic features
    features = []
    features.extend(p0_pits)             # 6 features
    features.extend(p1_pits)             # 6 features
    features.append(p0_kazan)            # 1 feature
    features.append(p1_kazan)            # 1 feature

    # Derived features
    features.append(sum(p0_pits))        # total stones P0
    features.append(sum(p1_pits))        # total stones P1
    features.append(p0_kazan - p1_kazan) # kazan difference
    features.append(int(current_player)) # whose turn

    # Replay opportunity feature
    replay_flag = 0
    for i in game.get_player_pits(current_player):
        stones = board[i]
        if stones == 0:
            continue
        landing_index = (i + stones) % 14
        if landing_index == game.get_kazan_index(current_player):
            replay_flag = 1
            break
    features.append(replay_flag)

    return np.array(features, dtype=np.float32)
