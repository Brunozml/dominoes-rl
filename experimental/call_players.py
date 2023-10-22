#! /usr/bin/env python
import dominoes
import subprocess



def simple_state(game): # HACKY SOLUTION: should not be here (dupliacated in QAgent.py)
    return [game.board.left_end(), game.board.right_end(), game.turn, game.hands]



def validated_input(prompt, validate_and_transform, error_message):
    '''
    Convenience wrapper around `input` that prompts the user until valid
    input is provided. Strips leading and trailing spaces from the input
    before applying any further processing.

    :param str prompt: prompt for input displayed to the user
    :param function validate_and_transform: function that takes as input the
                                            input provided by the user; returns
                                            None if the input is invalid;
                                            otherwise, returns the input,
                                            potentially after applying some
                                            processing to it
    :param str error_message: error message to display on invalid input
    :return: the user input, after `validate_and_transform` transforms it
    '''
    while True:
        user_input = input(prompt).strip()
        validated_user_input = validate_and_transform(user_input)

        if validated_user_input is not None:
            return validated_user_input

        print(error_message)

def validate_and_transform_target_score(target_score):
    '''
    To be used as a `validate_and_transform` function with `validated_input`.

    Requires that the input be a positive integer.

    :param str target_score: user input representing the target score
    :return: positive int representing the target score, if it is valid;
             None otherwise
    '''
    try:
        target_score = int(target_score)
    except ValueError:
        return None

    if target_score <= 0:
        return None

    return target_score

def validate_and_transform_nonnegative_index(sequence):
    '''
    Returns a function to be used as a `validate_and_transform`
    function with `validated_input`.
    '''
    def _validate_and_transform_nonnegative_index(i):
        '''
        To be used as a `validate_and_transform` function with `validated_input`.

        Requires that the input be a valid nonnegative index into `sequence`.

        :param str i: user input representing an index into `sequence`
        :return: the index as an integer, if it is valid; None otherwise
        '''
        if i not in (str(j) for j in range(len(sequence))):
            return None

        return int(i)

    return _validate_and_transform_nonnegative_index

def validate_and_transform_end(end):
    '''
    To be used as a `validate_and_transform` function with `validated_input`.

    Requires that the input be a valid end of the domino board - i.e. 'l' or 'r'.

    :param str end: user input representing an end of the domino board
    :return: True for the left end, False for the right end, None for invalid input
    '''
    end = end.lower()
    try:
        return {'l': True, 'r': False}[end]
    except KeyError:
        return None

# clear the terminal before starting the series
input('Welcome! Proceeding will clear all text from this terminal session.'
      ' If you are OK with this, press enter to continue.')
subprocess.call(['tput', 'reset'])

# start a new game with 6|6
game = dominoes.Game.new(starting_domino=dominoes.Domino(6, 6))

# player settings: human against rl agent

q_agent = dominoes.players.QAgent()
q_agent.train(n = 1000)
player_settings = [('Human', None),('AI: RL',q_agent),('AI: RL',q_agent),('AI: RL',q_agent) ] # TO-DO: remove redundancy



subprocess.call(['tput', 'reset'])

# game.result will be filled in once the game ends
while game.result is None:
    # print the game state so that all players can see it
    print('Board:')
    print(game.board)
    for player, hand in enumerate(game.hands):
        print('Player {} has {} dominoes in his/her hand.'.format(player, len(hand)))

    # clear the terminal upon starting a new turn
    input("It is now player {}'s turn. Press enter"
            " to continue.".format(game.turn))
    subprocess.call(['tput', 'reset'])

    # print the board so that the player can decide what to play
    print('Board:')
    print(game.board)

    # remember whose turn it currently is.
    # we'll need it after we move on to the next player.
    turn = game.turn

    # get the setting for the current player
    player_setting_name, player = player_settings[game.turn]

    if player is None:
        # the current player is a human. present the
        # player's hand in multiple-choice format.
        print("Player {}'s hand:".format(game.turn))
        hand = game.hands[game.turn]
        for i, d in enumerate(hand):
            print('{}) {}'.format(i, d))

        # ask what move they'd like to play,
        # until they select a valid move.
        while True:
            valid_inputs = list(range(len(hand)))
            d = hand[validated_input('Choose which domino you would like to play: ',
                                        validate_and_transform_nonnegative_index(hand),
                                        'Please enter a value in: {}'.format(valid_inputs))]

            if game.board:
                end = validated_input('Choose what end of the board you'
                                        ' would like to play on (l or r): ',
                                        validate_and_transform_end,
                                        'Please enter a value in: [l, r]')
            else:
                # if the board is empty, default to playing on the 'left'
                end = True

            try:
                game.make_move(d, end)
                break
            except dominoes.EndsMismatchException:
                # `game.make_move` is transactional - if it fails, the game
                # state is exactly as it was when the operation started
                print('The selected domino cannot be played on the'
                        ' selected end of the board. Please try again.')
    else:
        # the current player is an AI. apply the player setting to select a
        # move to play. the player setting is a callable that will sort the
        # game's valid moves in decreasing order of preference.

            # rl_state = simple_state(game).copy()

            # # choose an action to take based on the current state. no learning
            # action = q_agent.choose_action(rl_state, epsilon = False)

            # # unpack action to make move
            # move_tile, side = action

            action = q_agent(game)
            move_tile, side = action

            side_word = 'left' if side else 'right'
            print (f'Player {(game.turn -1)%4} chose to play {move_tile} on the {side_word} end of the board.')

            # game.make_move(move_tile, side)

        # # print out the selected move
        # print('Player {} ({}) chose to play {} on the {} end of the board.'.format(
        #     game.turn,
        #     player_setting_name,
        #     game.valid_moves[0][0],
        #     'left' if game.valid_moves[0][1] else 'right'
        # ))

        # # make the selected move
        # game.make_move(*game.valid_moves[0])

    # clear the terminal upon moving to the next
    # turn - no looking at the previous player's hand!
    input("Press enter to end player {}'s turn.".format(turn))
    subprocess.call(['tput', 'reset'])

# game over - move on to the next game
print('Game over!')
print(game, game.result)
