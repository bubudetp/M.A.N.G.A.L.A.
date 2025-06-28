from code.mangala_engine import MangalaGame
from code.kazanmaster_ai import KazanMasterAI
from test.random_ai import RandomAI

def simulate_game(ai0, ai1):
    game = MangalaGame()
    while not game.is_game_over():
        ai = ai0 if game.current_player == 0 else ai1
        move = ai.get_best_move(game)
        if move is not None:
            game.make_move(move)
    game.end_game()
    if game.board[6] > game.board[13]:
        return 0
    elif game.board[13] > game.board[6]:
        return 1
    else:
        return -1

def evaluate(ai0, ai1, num_games=50):
    results = {0: 0, 1: 0, -1: 0}
    for _ in range(num_games):
        winner = simulate_game(ai0, ai1)
        results[winner] += 1
    print(f"\nResults over {num_games} games:")
    print(f"AI0 wins: {results[0]}")
    print(f"AI1 wins: {results[1]}")
    print(f"Draws: {results[-1]}")

if __name__ == "__main__":
    evaluate(KazanMasterAI(max_depth=5), RandomAI(), num_games=20)
