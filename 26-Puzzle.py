import copy
import heapq


class Node:
    def __init__(self, state, goal_state, parent=None, action=None, depth=0, cost=0):
        self.state = state  # The state of the puzzle
        self.goal_state = goal_state  # The goal state of the puzzle
        self.parent = parent  # Reference to the parent node
        self.children = []  # List of references to the children nodes
        self.action = action # The action that led to this state (East, West, North, South, Up and Down)
        self.depth = depth  # The depth of the node in the search tree
        self.cost = cost  # The cumulative cost to reach this node
        self.h_value = self.calculate_heuristic() # The heuristic value for this node (h(n))

    def __lt__(self, other):
        # Used to compare the f(n) values of two nodes, used by the priority queue
        return self.cost + self.h_value < other.cost + other.h_value

    # Prints the node's state, action, depth, cost, and h(n) values
    def __repr__(self) -> str:
        return f"Node({self.state}, {self.action}, {self.depth}, {self.cost}, {self.h_value})\n"

    def is_goal(self, goal_state):
        # Check if the node's state matches the goal state
        return self.state == goal_state

    # Calculates the heuristic value using the Manhattan distance
    def calculate_heuristic(self):
        h_value = 0

        for layer in range(len(self.state)):
            for row in range(len(self.state[layer])):
                for col in range(len(self.state[layer][row])):
                    curr_pos = self.state[layer][row][col]

                    if curr_pos is not None:  # If position is not empty
                        # Iterate over layers, rows, and columns of the goal state
                        for goal_layer in range(len(self.goal_state)):
                            for goal_row in range(len(self.goal_state[goal_layer])):
                                for goal_col in range(len(self.goal_state[goal_layer][goal_row])):
                                    if curr_pos == self.goal_state[goal_layer][goal_row][goal_col]:
                                        # Manhattan distance
                                        h_value += abs(layer - goal_layer) + \
                                            abs(row - goal_row) + \
                                            abs(col - goal_col)
                                        break

        return h_value

    def get_depth_actions_fVals(self):
        # Retrieve the actions, f_values from the root node to this node through the parent references
        actions = []
        f_values = []

        current_node = self
        while current_node.parent:
            actions.append(current_node.action)
            f_values.append(current_node.cost + current_node.h_value)
            current_node = current_node.parent

        return [self.depth, actions[::-1], f_values[::-1]]

    def generate_child_nodes(self):
        child_nodes = []

        for layer in range(3):
            for i in range(3):
                for j in range(3):
                    if self.state[layer][i][j]==0:
                        # Found the empty space, now check valid moves

                        # Possible moves: [east, west, north, south, up, down]
                        moves = [(0, 1, "E"), (0, -1, "W"), (-1, 0, "N"),
                                 (1, 0, "S"), (0, 0, -1, "U"), (0, 0, 1, "D")]

                        for move in moves:
                            if len(move) == 3:
                                # Moving within the same grid
                                new_row, new_col = i + move[0], j + move[1]
                                if 0 <= new_row < 3 and 0 <= new_col < 3:
                                    # Create a copy of the current state to modify
                                    new_state = [[[cell for cell in row]
                                                  for row in grid] for grid in self.state]
                                    # Swap the empty space with the neighboring tile
                                    new_state[layer][i][j], new_state[layer][new_row][new_col] = new_state[
                                        layer][new_row][new_col], new_state[layer][i][j]
                                    # Create a new Node representing the successor state
                                    successor_node = Node(
                                        new_state, goal_state=self.goal_state, parent=self, action=move[2], depth=self.depth + 1, cost=self.cost + 1)
                                    child_nodes.append(successor_node)
                            elif len(move) == 4:
                                # Moving between layers
                                new_layer = layer + move[2]
                                if 0 <= new_layer < 3:
                                    # Create a copy of the current state to modify
                                    new_state = [[[cell for cell in row]
                                                  for row in grid] for grid in self.state]
                                    # Swap the empty space between layers
                                    new_state[layer][i][j], new_state[new_layer][i][j] = new_state[new_layer][i][j], new_state[layer][i][j]
                                    # Create a new Node representing the successor state
                                    successor_node = Node(
                                        new_state, goal_state=self.goal_state, parent=self, action=move[3], depth=self.depth + 1, cost=self.cost + 1)
                                    child_nodes.append(successor_node)

        return child_nodes

# Priority queue implementation using heapq
# The priority queue is used to store the nodes that are generated during the A* search
# The nodes are stored in the priority queue based on their f(n) values
class PriorityQueue:
    def __init__(self):
        self.elements = []

    def is_empty(self):
        return not self.elements

    # Heap will maintain the minimum f(n) value at the root as well as the the Node object associated with it
    def put(self, node):
        heapq.heappush(self.elements, (node.cost + node.h_value, node))

    def get(self):
        return heapq.heappop(self.elements)

def AStar_search(initial_state, goal_state):
    visited = set()  # Set to store visited states
    frontier = PriorityQueue()
    initial_node = Node(initial_state, goal_state)
    frontier.put(initial_node)

    # Convert the current node's state to a hashable object
    hashable_node_state = tuple(map(lambda sublist: tuple(map(tuple, sublist)), initial_node.state))
    visited.add(hashable_node_state)

    nodes_generated = 1

    while not frontier.is_empty():
        f_val, current_node = frontier.get()

        if current_node.is_goal(goal_state):
            # Found the goal state
            return current_node.get_depth_actions_fVals(), nodes_generated

        # Generate successor states and add them to the priority queue
        successor_states = current_node.generate_child_nodes()
        for successor in successor_states:
            hashable_node_state = tuple(map(lambda sublist: tuple(map(tuple, sublist)), successor.state))
            if hashable_node_state not in visited:
                frontier.put(successor)
                visited.add(hashable_node_state)
                nodes_generated += 1

    # If the priority queue becomes empty and the goal is not reached, the puzzle is unsolvable
    return None, nodes_generated

# Converts the input text into 2 lists of lists, one for the puzzle state and one for the goal state
def parse_input():
    # Opens and reads the input file
    with open("Input1.txt", "r") as file:
        input_text = file.read()

    # Splits the input text into individual grid sections
    grid_layers = input_text.strip().split('\n\n')

    # Parses each grid section and convert it to a list of lists
    puzzle_state = []
    for layer in grid_layers:
        grid = []
        lines = layer.split('\n')
        for line in lines:
            values = line.split()
            row = [int(value) for value in values]
            grid.append(row)
        puzzle_state.append(grid)

    initial_state = puzzle_state[:3]
    goal_state = puzzle_state[3:]

    return initial_state, goal_state


def main():
    initial_state, goal_state = parse_input()
    results, nodes_generated = AStar_search(initial_state, goal_state)
    depth, actions, f_values = results

    # Output solution
    with open("Output1.txt", "w") as file:
        # Initial State Tile Pattern
        for grid in initial_state:
            for row in grid:
                file.write(" ".join(map(str, row)) + "\n")
            file.write("\n")
        # Goal State Tile Pattern
        for grid in goal_state:
            for row in grid:
                file.write(" ".join(map(str, row)) + "\n")
            file.write("\n")
        # Depth level d of the shallowest goal node
        file.write(f"{depth}\n")
        # Total number of nodes N generated in your tree
        file.write(f"{nodes_generated}\n")
        # Solution: Sequence of actions from root node to goal node
        file.write(" ".join(actions) + "\n")
        # f(n) values of the nodes along the solution path, from the root node to the goal node
        file.write(" ".join(map(str, f_values)) + "\n")

main()
