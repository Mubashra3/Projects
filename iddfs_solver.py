'''
Homework 4: 15-Puzzle Solver using IDDFS
Name: Mubashra Sohail
netid: msoha3
Description: This program solves the 15-puzzle problem using the Iterative Deepening
             Depth-First Search (IDDFS) algorithm. It follows the structure requested
             in the assignment, using a recursive DLS and path-checking to find the
             optimal solution.
'''
import math
import time
import psutil
import os
import sys

# This class defines the state of the problem in terms of board configuration
class Board:
    def __init__(self, tiles):
        self.size = int(math.sqrt(len(tiles)))
        self.tiles = tuple(tiles) # Use a tuple to make the state immutable and hashable

    # This function returns the resulting state from taking a particular action
    def execute_action(self, action):
        new_tiles = list(self.tiles)
        empty_index = new_tiles.index(0)
        
        row, col = empty_index // self.size, empty_index % self.size

        if action == 'L' and col > 0:
            swap_idx = empty_index - 1
        elif action == 'R' and col < self.size - 1:
            swap_idx = empty_index + 1
        elif action == 'U' and row > 0:
            swap_idx = empty_index - self.size
        elif action == 'D' and row < self.size - 1:
            swap_idx = empty_index + self.size
        else:
            return None # Invalid move

        new_tiles[empty_index], new_tiles[swap_idx] = new_tiles[swap_idx], new_tiles[empty_index]
        return Board(new_tiles)

# This class defines the node on the search tree
class Node:
    def __init__(self, state, parent, action, depth=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.depth = depth

    # Returns string representation of the state
    def __repr__(self):
        return str(self.state.tiles)

    # Comparing nodes based on their states
    def __eq__(self, other):
        return self.state.tiles == other.state.tiles

    def __hash__(self):
        return hash(self.state.tiles)

# This function returns the list of children from the parent node
def get_children(parent_node):
    children = []
    actions = ['L', 'R', 'U', 'D']
    for action in actions:
        child_state = parent_node.state.execute_action(action)
        if child_state: # Only add if the move was valid
            child_node = Node(child_state, parent_node, action, parent_node.depth + 1)
            children.append(child_node)
    return children

# This function backtracks to find the solution path
def find_path(node):
    path = []
    while node.parent is not None:
        path.append(node.action)
        node = node.parent
    path.reverse()
    return path

# This function checks for cycles by looking at ancestors
def is_cycle(node):
    current = node.parent
    while current:
        if node.state == current.state:
            return True
        current = current.parent
    return False

# This is the main IDDFS algorithm
def iterative_deepening_search(root_node):
    start_time = time.time()
    total_expanded_nodes = 0
    max_memory = 0
    
    # The main loop of IDDFS: increase the depth limit in each iteration
    for depth_limit in range(sys.maxsize):
        frontier = [root_node]
        # This set is used to prune paths that have already been explored in the current DLS
        # For tree search version of IDDFS, this can be removed.
        # For graph search, it avoids re-exploring within the same DLS iteration.
        explored_in_dls = set() 
        
        # --- Start of Depth-Limited Search (DLS) for the current depth_limit ---
        while frontier:
            max_memory = max(max_memory, sys.getsizeof(frontier) + sys.getsizeof(explored_in_dls))
            current_node = frontier.pop()
            
            # The goal check
            if goal_test(current_node.state.tiles):
                path = find_path(current_node)
                end_time = time.time()
                return path, total_expanded_nodes, (end_time - start_time), max_memory
            
            # Pruning based on depth limit
            if current_node.depth >= depth_limit:
                continue

            total_expanded_nodes += 1
            explored_in_dls.add(current_node.state.tiles)

            # Expand children in reverse to explore in L, R, U, D order
            for child in reversed(get_children(current_node)):
                if child.state.tiles not in explored_in_dls and not is_cycle(child):
                    frontier.append(child)
        # --- End of DLS ---

# Main function to run the solver
def main():
    try:
        initial_str = input("Enter the initial configuration (16 numbers separated by spaces, 0 for blank): ")
        initial_list = [int(n) for n in initial_str.split()]
        if len(initial_list) != 16 or set(initial_list) != set(range(16)):
            raise ValueError
    except ValueError:
        print("Invalid input. Please enter 16 unique numbers from 0 to 15.")
        return

    root_board = Board(initial_list)
    root_node = Node(root_board, None, None, 0)
    
    # Call the main search function
    result = iterative_deepening_search(root_node)

    if result:
        path, expanded_nodes, time_taken, memory_consumed = result
        print("\n--- Solution Found! ---")
        print(f"Moves: {' '.join(path)}")
        print(f"Number of expanded Nodes: {expanded_nodes}")
        print(f"Time Taken: {time_taken:.4f} seconds")
        print(f"Max Memory (Bytes): {memory_consumed}")
    else:
        print("Could not find a solution.")

# Utility function to check for the goal state
def goal_test(current_tiles):
    return current_tiles == tuple(range(1, 16)) + (0,)

if __name__ == "__main__":
    main()