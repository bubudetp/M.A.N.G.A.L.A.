from code.mangala_engine import MangalaGame
from code.ai.kazanmaster_ai import KazanMasterAI
from test.random_ai import RandomAI
from test.greedy_ai import GreedyAI
from test.rolloutless_kazan import RolloutlessKazanAI

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


def run_match(ai0, ai1, games=20):
    wins = [0, 0]
    draws = 0

    for i in range(games):
        game = MangalaGame()
        players = [ai0, ai1]
        while not game.is_game_over():
            current_ai = players[game.current_player]
            move = current_ai.get_best_move(game)
            game.make_move(move)
        game.end_game()
        p0, p1 = game.board[6], game.board[13]
        if p0 > p1:
            wins[0] += 1
        elif p1 > p0:
            wins[1] += 1
        else:
            draws += 1

    print(f"\nResults over {games} games:")
    print(f"AI0 wins: {wins[0]}")
    print(f"AI1 wins: {wins[1]}")
    print(f"Draws: {draws}")

if __name__ == "__main__":
    ai0 = KazanMasterAI(max_depth=5)
    ai1 = GreedyAI()

    run_match(ai0, ai1, games=50)