class Node:
    def __init__(self, state, parent=None, action=None, depth=0, cost=0, heuristic=0):
        self.state = state  # The state of the puzzle
        self.parent = parent  # Reference to the parent node
        self.action = action  # The action that led to this state (e.g., 'move up', 'move left', etc.)
        self.depth = depth  # The depth of the node in the search tree
        self.cost = cost  # The cumulative cost to reach this node
        self.heuristic = heuristic  # The heuristic value for this node (used in informed search)

    def __lt__(self, other):
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)

    def is_goal(self, goal_state):
        # Check if the node's state matches the goal state
        return self.state == goal_state

    def get_path(self):
        # Retrieve the path from the root node to this node
        path = [self]
        current_node = self
        while current_node.parent:
            path.insert(0, current_node.parent)
            current_node = current_node.parent
        return path

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
            row = [int(value) if value != '0' else None for value in values]
            grid.append(row)
        puzzle_state.append(grid)

    goal_state = puzzle_state[3:]
    puzzle_state = puzzle_state[:3]

    # Prints the parsed puzzle state
    for grid in puzzle_state:
        for row in grid:
            print(row)
        print()
    
    # Prints the parsed goal state
    for grid in goal_state:
        for row in grid:
            print(row)
        print()

def main():
    parse_input()

main()