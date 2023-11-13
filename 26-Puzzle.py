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

# Define possible moves
moves = [(0, 1, 'E'), (0, -1, 'W'),  (-1, 0, 'N'), (1, 0, 'S'), (-1, 0, 'U'), (1, 0, 'D')]

# Generates the possible moves from the current state of the puzzle
def actions(state):
    # Find position of the empty cell in the puzzle
    empty_cell = None
    for x in range(len(state)):
        for y in range(len(state[i])):
            if state[x][y] is None:
                empty_cell = (x, y)
                break
        if empty_cell:
            break

    # Keep track of actions and calculate all changes in row and column positions when making a move
    actions = []
    for row, col, action in moves:
        next_x, next_y = empty_cell[0] + row, empty_cell[1] + col
        # Check is move is valid, apply it, and append the new state to your actions list
        if 0 <= next_x < len(state) and 0 <= new_y < len(state[0]):
            next_state = [list(row) for row in state]
            next_state[empty_cell[0]][empty_cell[1]], next_state[next_x][next_y] = next_state[next_x][new_y], next_state[empty_cell[0]][empty_cell[1]]
            actions.append((next_state, action))

    return actions

# Calculates the heuristic value using the Manhattan distance
def h_val(curr_state, goal_state):
    h_value = 0  
    # Iterate over rows and columns of the current state and store the current position
    for row in range(len(curr_state)):
        for col in range(len(curr_state[i])):
            curr_pos = state[i][j]

            if curr_pos is not None:    # If position is not empty
                # Iterate over rows and columns of the goal state and apply Manhattan distance h val
                for goal_row in range(len(goal_state)): 
                    for goal_col in range(len(goal_state[goal_row])):
                        if curr_pos == goal_state[goal_row][goal_co]:
                            h_value += abs(row - goal_row) + abs(col - goal_col)  # Manhattan distance
                            break
    return h_value

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
    # puzzle_state, goal_state = parse_input()
    # root = Node(puzzle_state)

    initial_state, goal_state = parse_input()
    path, actions, f_values, generated_nodes = astar_search(initial_state, goal_state)

    # Output solution
    with open("output.txt", "w") as file:
        # Initial State Tile Pattern
        for row in initial_state:
            file.write("".join(map(str, row)) + "\n")
        # Goal State Tile Pattern
        for row in goal_state:
            file.write("".join(map(str, row)) + "\n")
        # Blank Line
        file.write("\n")
        # Depth level d of the shallowest goal node
        file.write(f"{path[0].depth}\n")
        # Total number of nodes N generated in your tree
        file.write(f"{generated_nodes}\n")
        # Solution: Sequence of actions from root node to goal node
        file.write(" ".join(actions) + "\n")
        # f(n) values of the nodes along the solution path, from the root node to the goal node
        file.write(" ".join(map(str, f_values)) + "\n")

main()