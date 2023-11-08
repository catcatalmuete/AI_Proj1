import heapq

class Node:
    def __init__(self, state, parent=None, action=None, depth=0, cost=0, hVal=0):
        self.state = state  # The state of the puzzle
        self.parent = parent  # Reference to the parent node
        self.children = []  # List of references to the children nodes
        self.action = action  # The action that led to this state (East, West, North, South, Up and Down)
        self.depth = depth  # The depth of the node in the search tree
        self.cost = cost  # The cumulative cost to reach this node
        self.hVal = hVal  # The heuristic value for this node (h(n))

    def __lt__(self, other):
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)

    def is_goal(self, goal_state):
        # Check if the node's state matches the goal state
        return self.state == goal_state

    def get_path_actions_fVals(self):
        # Retrieve the path from the root node to this node
        path = []
        actions = []
        f_values = []

        current_node = self
        while current_node.parent:
            path.append(current_node)
            actions.append(current_node.action)
            f_values.append(current_node.cost + current_node.hVal)
            current_node = current_node.parent

        return [path[::-1], actions[::-1], f_values[::-1]]
    
    # def get_children(self):
        
# Priority queue implementation using heapq
# The priority queue is used to store the nodes that are generated during the search
# The nodes are stored in the priority queue based on their f(n) values
class PriorityQueue:
    def __init__(self):
        self.elements = []

    def is_empty(self):
        return not self.elements

    # Heap will maintain the minimum f(n) value at the root as well as the the Node object associated with it
    def put(self, node):
        heapq.heappush(self.elements, (node.cost + node.hVal, node))

    def get(self):
        return heapq.heappop(self.elements)

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

    return puzzle_state, goal_state

def main():
    puzzle_state, goal_state = parse_input()
    root = Node(puzzle_state)


main()