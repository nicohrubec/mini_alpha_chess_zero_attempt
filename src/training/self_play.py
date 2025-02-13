from copy import deepcopy

import numpy as np
import torch

from training.Player import Player


def play_n_self_play_games(game, n_games=100, max_game_length=100, n_playouts=10):
    # init best player here and let it play against itself
    # --> either randomly initialized or load in an already trained model
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    # TODO: load in current best version of neural net
    curr_best_player = Player(device=device)

    for i in range(n_games):
        player = deepcopy(curr_best_player)
        play_self_play_game(game, player, max_game_length, n_playouts)

    # TODO: train neural network --> pick batches from generated self play samples
    # TODO: evaluation --> pit new neural net against previous version and replace if successful
    # Skeleton for needed method in Player class.


def play_self_play_game(game, player, max_game_length=100, n_playouts=10):

    while not game.is_checkmate() and game.get_num_moves() < max_game_length and not game.is_game_ended():
        move_value_dict = get_move_values(game, player, n_playouts, max_game_length)  # get action value dict
        move = pick_move(move_value_dict)
        game.make_move(move)


def get_move_values(game, player, n_playouts, max_game_length):
    move_values = {}
    visited = {}

    for move in game.get_legal_moves():
        # monte carlo value for move determined by mean over n rollouts starting from new state after picking the move
        game.make_move(move)
        move_values[str(move)] = np.mean([do_playout(game, player, visited, max_game_length)
                                          for i in range(0, n_playouts)])
        # get back to actual state
        game.undo_last_move()

    print(move_values)

    return move_values


def do_playout(game, player, visited, max_game_length):
    if game.is_checkmate():
        player.log([game.get_state(), -1])  # current player lost --> value -1
        return -1
    elif game.get_num_moves() > max_game_length:
        value = -player.predict(game.get_state())

        return -value
    elif game.is_game_ended():  # check for draw --> stalemate, insufficient material, repetitions etc
        return 0

    if hash(game) not in visited:  # new state encountered
        visited[hash(game)] = 1
        value = player.predict(game.get_state())

        return -value
    else:  # state was already visited
        visited[hash(game)] += 1

    heuristic_move_values = {}

    for move in game.get_legal_moves():
        game.make_move(move)
        # get approximated value for new state
        heuristic_move_values[str(move)] = get_heuristic_state_value(game, player)
        game.undo_last_move()

    # play on
    # print(heuristic_move_values)
    # print(game.get_num_moves())
    move = pick_move(heuristic_move_values)
    game.make_move(move)
    value = -do_playout(game, player, visited, max_game_length)
    game.undo_last_move()

    # add state value pair to training samples
    player.log([game.get_state(), value])

    return value  # return the playout value


def get_heuristic_state_value(game, player):
    state = game.get_state()
    heuristic_value = player.predict(state)

    return heuristic_value


# logic for how to pick the move during self play
# for now just pick action with highest value
def pick_move(value_dict):
    return max(value_dict, key=value_dict.get)
