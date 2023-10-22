import dominoes


#%%

#should fix this correctly

def available_actions(state):
    """
    Important function! should implement as method.
    uses game state to return list of available actions for the current
    player
    """
    left, right, turn, hands = state
    actions = set()
    for domino in hands[turn]:
        if left in domino:
            actions.add((domino, True))
        if right in domino:
            actions.add((domino, False))
    return actions

#%%

q_agent = dominoes.players.QAgent()
q_agent.train(n = 100)

game = dominoes.Game.new(starting_domino=dominoes.Domino(6, 6))

r_player = dominoes.players.random
omniscient_player = dominoes.players.omniscient()


player_settings = [('AI: q-agent', q_agent),
                   ('AI: random', r_player), 
                   ('AI: random', r_player), 
                   ('AI: random' , r_player)]



def single_game(player_settings):
    """
    automatically runs a single game, with the four players specified 
    in the "player_settings" argument. 
    returns the game object of the played game.
    
    """
    
    single_game = dominoes.Game.new(starting_domino= dominoes.Domino(6,6))

    while single_game.result is None: 
            # remember whose turn it currently is.
            # we'll need it after we move on to the next player.
            turn = single_game.turn

            # get the setting for the current player
            player_setting_name, player_type = player_settings[single_game.turn]

            # the current player is an AI. apply the player setting to select a
            # move to play and make the selected move
            player_type(single_game)

            # print out the selected move
            print('Player {} ({}) chose to play {} on the {} end of the board.'.format(
                game.turn,
                player_setting_name,
                game.valid_moves[0][0],
                'left' if game.valid_moves[0][1] else 'right'
            ))

            # make the selected move
            single_game.make_move(*game.valid_moves[0])
    
    return single_game

#%%
# single_game(player_settings)

#%%

# new game wi

single_game(player_settings)