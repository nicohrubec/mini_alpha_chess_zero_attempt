import chess
from training.state import State
from training.self_play import play_self_play_game, play_n_self_play_games

if __name__ == '__main__':
    board = chess.Board()
    game = State(board)

    play_n_self_play_games(game, n_games=1, max_game_length=5, n_playouts=2)
