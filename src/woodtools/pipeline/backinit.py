"""
Initialize the global variables backend for the GUI widgets.

@Author: Jannik Stebani
"""

def init_globals():
    """
    Initialize the global variables for the GUI widgets.
    This function sets up a dictionary to store the current object
    and its parameters, which can be accessed by other parts of the code.
    """
    globals()['__CURRENT_OBJECT__'] = {}
    globals()['__CURRENT_OBJECT__']['ID'] = None
    globals()['__CURRENT_OBJECT__']['volume'] = None
    globals()['__PARAMETERS__'] = {}