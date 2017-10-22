
from mcts_node import MCTSNode
from random import choice
from math import sqrt, log

num_nodes = 1000
explore_faction = 2.

def traverse_nodes(node, board, state, identity):
    """ Traverses the tree until the end criterion are met.

    Args:
        node:       A tree node from which the search is traversing.
        board:      The game setup.
        state:      The state of the game.
        identity:   The bot's identity, either 'red' or 'blue'.

    Returns:        A node from which the next stage of the search can proceed.

    """

    want_node_val = 0
    best = {}

    leaf_node = node
    explore = lambda w, n, t, c: (w / n) + (c * sqrt((log(t) / n)))
    values = []
    bestest = 0

    count = 0
    while node.visits and node.child_nodes:
        for child in node.child_nodes:
            values[count] = explore(child.wins, child.visits, node.visits, explore_faction)
            best[values[count]] = child
            count += 1
        count = 0

        for value in values:
            if bestest < value:
                bestest = value
                leaf_node = best[values[count]]
            count += 1
        count = 0
        node = leaf_node
    return leaf_node

    """
    while node.child_nodes:
    while not board.is_ended(state):
        for child in node.child_nodes:
            best[child.value()] = explore(child.wins, child.visits, node.visits, explore_faction)

        for value in best:
            if best[value] > want_node_val:
                leaf_node = value
                want_node_val = best[value]

    return leaf_node
    # Hint: return leaf_node
    """

def expand_leaf(node, board, state):
    """ Adds a new leaf to the tree by creating a new child node for the given node.

    Args:
        node:   The node for which a child will be added.
        board:  The game setup.
        state:  The state of the game.

    Returns:    The added child node.

    """
    node.__repr__()
    print()
    print(node)
    print()
    actions = board.legal_actions(state)
    action = choice(actions)

    new_node = MCTSNode(node, action, actions)
    node.child_nodes[action] = new_node
    return new_node


def rollout(board, state):
    """ Given the state of the game, the rollout plays out the remainder randomly.

    Args:
        board:  The game setup.
        state:  The state of the game.

    """
    while not board.is_ended():
        action = choice(board.legal_actions(state))
        state = board.next_state(state, action)


def backpropagate(node, won):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.

    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.

    """
    if won:
        node.wins += 1
    node.visits += 1

    if node.parent is not None:
        backpropagate(node.parent, won)


def think(board, state):
    """ Performs MCTS by sampling games and calling the appropriate functions to construct the game tree.

    Args:
        board:  The game setup.
        state:  The state of the game.

    Returns:    The action to be taken.

    """
    identity_of_bot = board.current_player(state)
    root_node = MCTSNode(parent=None, parent_action=None, action_list=board.legal_actions(state))
    sampled_game = None

    for step in range(num_nodes):
        # Copy the game for sampling a playthrough
        sampled_game = state

        # Start at root
        node = root_node

        # Do MCTS - This is all you!
        leaf = traverse_nodes(node, board, sampled_game, identity_of_bot)

        new_node = expand_leaf(leaf, board, sampled_game)

        rollout(board, sampled_game)

        player = board.current_player(sampled_game)
        if player == identity_of_bot:
            backpropagate(new_node, True)
        else:
            backpropagate(new_node, False)


    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.
    return leaf
