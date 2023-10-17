import dominoes_lib as dominoes

def simple_state(game):
    """
    Return a simple state representation for the game `game`.
    """
    return game.board.left_end(), game.board.right_end()

