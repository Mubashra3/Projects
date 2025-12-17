'''
Homework 5: 15-Puzzle Solver using A* Number of Misplaced Tiles
Name: Mubashra Sohail
netidL msoha3
'''

import time
import psutil, os
from queue import PriorityQueue

# --- Node Class ---
# Added __lt__ for the PriorityQueue to compare nodes
class Node:
    def __init__(self, state, parent, operator, depth):
        self.state = state
        self.parent = parent
        self.operator = operator
        self.depth = depth
        # f_cost will store g(n) + h(n)
        self.f_cost = 0

    # Less-than comparison for PriorityQueue sorting
    def __lt__(self, other):
        return self.f_cost < other.f_cost

# --- State and Move Functions ---
def move_right(state):
    new_state = state[:]
    index = new_state.index(0)
    if index not in [3, 7, 11, 15]:
        new_state[index + 1], new_state[index] = new_state[index], new_state[index + 1]
        return new_state
    return None

def move_left(state):
    new_state = state[:]
    index = new_state.index(0)
    if index not in [0, 4, 8, 12]:
        new_state[index - 1], new_state[index] = new_state[index], new_state[index - 1]
        return new_state
    return None

def move_up(state):
    new_state = state[:]
    index = new_state.index(0)
    if index not in [0, 1, 2, 3]:
        new_state[index - 4], new_state[index] = new_state[index], new_state[index - 4]
        return new_state
    return None

def move_down(state):
    new_state = state[:]
    index = new_state.index(0)
    if index not in [12, 13, 14, 15]:
        new_state[index + 4], new_state[index] = new_state[index], new_state[index + 4]
        return new_state
    return None

def expand_node(node):
    expanded_nodes = []
    # Create nodes for each possible move
    up_state = move_up(node.state)
    if up_state:
        expanded_nodes.append(Node(up_state, node, "U", node.depth + 1))
    
    down_state = move_down(node.state)
    if down_state:
        expanded_nodes.append(Node(down_state, node, "D", node.depth + 1))

    left_state = move_left(node.state)
    if left_state:
        expanded_nodes.append(Node(left_state, node, "L", node.depth + 1))

    right_state = move_right(node.state)
    if right_state:
        expanded_nodes.append(Node(right_state, node, "R", node.depth + 1))
        
    return expanded_nodes

# --- Heuristic Function ---
def h_misplaced_tiles(state, goal):
    cost = 0
    for i in range(len(state)):
        if state[i] != 0 and state[i] != goal[i]:
            cost += 1
    return cost

# --- A* Search Algorithm ---
def a_star(start_state, goal_state):
    process = psutil.Process(os.getpid())
    memory_before = process.memory_info().rss / 1024.0
    
    # Use a PriorityQueue for the frontier
    frontier = PriorityQueue()
    
    # Use a set for the explored list for fast lookups
    explored = set()
    
    nodes_expanded = 0
    start_node = Node(start_state, None, None, 0)
    start_node.f_cost = start_node.depth + h_misplaced_tiles(start_state, goal_state)
    
    frontier.put(start_node)

    while not frontier.empty():
        current_node = frontier.get()
        
        # Add the string representation of the state to explored set
        explored.add(tuple(current_node.state))
        
        if current_node.state == goal_state:
            memory_after = process.memory_info().rss / 1024.0
            
            # Reconstruct path
            path = []
            temp = current_node
            while temp.parent:
                path.append(temp.operator)
                temp = temp.parent
            path.reverse()

            print(f"The number of nodes expanded: {nodes_expanded}")
            print(f"Memory elapsed: {memory_after - memory_before:.2f} kb")
            return path

        nodes_expanded += 1
        
        for child_node in expand_node(current_node):
            if tuple(child_node.state) not in explored:
                # Calculate g(n) + h(n)
                child_node.f_cost = child_node.depth + h_misplaced_tiles(child_node.state, goal_state)
                frontier.put(child_node)
    
    return None # No solution found

# --- Main Method ---
def main():
    final_state = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]

    # Get manual input from the user
    print("Enter the initial state of the 15-puzzle (16 numbers from 0-15 separated by spaces):")
    try:
        start_state_str = input("> ")
        start_state = [int(i) for i in start_state_str.split()]
        if len(start_state) != 16 or set(start_state) != set(range(16)):
            raise ValueError
    except ValueError:
        print("Invalid input. Please enter 16 unique numbers from 0-15.")
        return

    start_time = time.time()
    result = a_star(start_state, final_state)
    end_time = time.time()
    
    if result:
        print("\nMoves:", "".join(result))
        print(len(result), "moves")
    else:
        print("No solution found.")
        
    print(f"Total searching time: {round((end_time - start_time), 3)} seconds")

if __name__ == "__main__":
    main()