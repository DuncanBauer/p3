
from mcts_node import MCTSNode
from random import choice
from math import sqrt, log

num_nodes = 996
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
    print("Traverse root node: ")
    print(node)
    best = {}

    leaf_node = node
    explore = lambda w, n, t, c: (w / n) + (c * sqrt((log(t) / n)))
    values = []
    bestest = 0

    while node.visits and node.child_nodes:
        for child in node.child_nodes:
            """
            print("Child in traverse: ")
            print(child)
            print("Real child?: ")
            print(node.child_nodes[child])
            """
            best[child] = explore(node.child_nodes[child].wins, node.child_nodes[child].visits, node.visits, explore_faction)
            #values.append(explore(node.child_nodes[child].wins, node.child_nodes[child].visits, node.visits, explore_faction))
            #best[values[count]] = child

        for child in best:
            if best[child] > bestest:
                bestest = best[child]
                leaf_node = node.child_nodes[child]
        node = leaf_node

    print("Traverse return leaf: ")
    print(leaf_node)

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
    """print()
    print("Expanding on leaf: ")
    print(node)
    print()"""
    actions = board.legal_actions(state)
    action = choice(actions)

    new_node = MCTSNode(node, action, actions)
    #print("New leaf: ")
    #print(new_node)
    node.child_nodes[action] = new_node
    return new_node


def rollout(board, state):
    """ Given the state of the game, the rollout plays out the remainder randomly.

    Args:
        board:  The game setup.
        state:  The state of the game.

    """
    while not board.is_ended(state):
        #print(board.legal_actions(state))
        action = choice(board.legal_actions(state))
        #print(action)
        state = board.next_state(state, action)
        #print(board.display(state,action))
        #input("Press enter to continue...")
    return state


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

        print("Game state: ")
        print(sampled_game)
        sampled_game = rollout(board, sampled_game)
        print("Game state: ")
        print(sampled_game)
        #rollout(board, sampled_game)
        """
        print()
        print()
        print()
        print()
        print()
        print()
        print("GAME OVER")
        print()
        print()
        print()
        print()
        print()
        print()
        """
        player = board.current_player(sampled_game)
        won = False
        if player == identity_of_bot:
            won = True
        backpropagate(new_node, won)

    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.
    return choice(board.legal_actions(state))
