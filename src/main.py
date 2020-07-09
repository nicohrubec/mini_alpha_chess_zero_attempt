import chess

from training.self_play import play_n_self_play_games
from training.state import State

if __name__ == '__main__':
    board = chess.Board()
    game = State(board)

    while True:  # self play
        play_n_self_play_games(game, n_games=1, max_game_length=60, n_playouts=10)

    # TODO: Add frontend with possibility to play against current best player.
