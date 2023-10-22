"""
experimental script for playing against my trained agent.

"""

import dominoes

q_agent = dominoes.players.QAgent()
q_agent.train(n = 100)

r_player = dominoes.players.random
omniscient_player = dominoes.players.omniscient()


player_settings = [('AI: q-agent', q_agent),
                   ('AI: random', r_player), 
                   ('AI: random', r_player), 
                   ('AI: random' , r_player)]


player_settings = [('AI: q-agent', q_agent),
                   ('AI: random', q_agent), 
                   ('AI: random', q_agent), 
                   ('AI: random' , q_agent)]


def single_game(player_settings):
    """
    automatically runs a single game, with the four players specified 
    in the "player_settings" argument. 
    returns the game object of the played game.
    
    """
    
    game = dominoes.Game.new(starting_domino= dominoes.Domino(6,6))

    while game.result is None: 
            # remember whose turn it currently is.
            # we'll need it after we move on to the next player.
            turn = game.turn

            # get the setting for the current player
            player_setting_name, player_type = player_settings[game.turn]

            # the current player is an AI. apply the player setting to select a
            # move to play and make the selected move
            player_type(game)

            # make the selected move
            game.make_move(*game.valid_moves[0])
    
    return game

#%%
# single_game(player_settings)

#%%
