import math
import heapq
import queue
import copy

import time
import tkinter as tk
class PuzzleNode:
    def __init__(self, state, parent=None, move=None, cost=0, heuristic=0):
        self.state = state
        self.parent = parent
        self.move = move
        self.cost = cost
        self.heuristic = heuristic
        if parent != None:
            self.depth = parent.depth + 1
        else:
            self.depth = 0

    def __lt__(self, other):
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)
    def incrementDepth(self):
        self.depth += 1
    def getDepth(self):
        return self.depth
    
def checkSolvable(state,goal_state):
    inversions = 0
    linearList = []
    for i in range(0,3):
        for j in range(0,3):
            if(state[i][j] != 0):
                linearList.append(state[i][j])
    for i in range(0,len(linearList)):
        for j in range(i+1,len(linearList)):
            if(linearList[i] > linearList[j]):
                inversions += 1
    print(f'The number of inversions = {inversions}')
    if (inversions) % 2 == 0:
        return True
    return False
def get_goal_pos(value,goal_state):
    size=3
    for i in range(size):
        for j in range (size):
            if value == goal_state[i][j]:
                return (i,j)
def manhattan_distance(state, goal_state):
    distance = 0
    size = 3
    for i in range(size):
        for j in range(size):
            value = state[i][j]
            if value != 0:
                goal_position = get_goal_pos(value,goal_state)
                distance += abs(i - goal_position[0]) + abs(j - goal_position[1])
    return distance
def eucledian_distance(state,goal_state):
    distance=0
    size=3
    for i in range(size):
        for j in range (size):
            value=state[i][j]
            if value !=0:
                goal_position = get_goal_pos(value,goal_state)
                distance+=math.sqrt(math.pow(i-goal_position[0],2)+math.pow(j-goal_position[1],2))
    return  distance


def generate_neighbors(node,func):
    neighbors = []
    size = len(node.state)
    zero_position = next((i, j) for i, row in enumerate(node.state) for j, val in enumerate(row) if val == 0)

    for move in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        new_position = (zero_position[0] + move[0], zero_position[1] + move[1])

        if 0 <= new_position[0] < size and 0 <= new_position[1] < size:
            new_state = [row[:] for row in node.state]
            new_state[zero_position[0]][zero_position[1]] = node.state[new_position[0]][new_position[1]]
            new_state[new_position[0]][new_position[1]] = 0
            if func==None:
                neighbors.append(PuzzleNode(new_state, parent=node, move=move, cost=node.cost + 1,heuristic=None))
            else:
                neighbors.append(PuzzleNode(new_state, parent=node, move=move, cost=node.cost + 1, heuristic=func(new_state, goal_state)))
    return neighbors
def arrayStates(array):
    a=[]
    for s in array:
        a.append(s.state)
    return a
def BFS(initial_state,goal_state):
    if(checkSolvable(initial_state,goal_state) == False):
        print('This puzzle is unsolvable!')
        return None,[]
    else:
        initial_node=PuzzleNode(initial_state,parent=None,move=None,cost=0,heuristic=None)
        frontier=[]
        depth=0
        closed_set = set()
        other_set = set()
        frontier.append(initial_node)
        explored=[]
        maxDepth=0
        while frontier:
            current_node=frontier.pop(0)
            other_set.add(tuple(map(tuple, current_node.state)))
            explored.append(current_node)
            other_set.add(tuple(map(tuple, current_node.state)))
            if current_node.getDepth()>maxDepth:
                maxDepth=current_node.getDepth()
            if current_node.state == goal_state:
                path = []
                print(f'The current depth:{current_node.getDepth()}')
                while current_node != None:
                    path.append((current_node.state, current_node.move))
                    current_node=current_node.parent
                return path[::-1],arrayStates(explored),maxDepth
            else:
                closed_set.add(tuple(map(tuple, current_node.state)))
                neighbours=generate_neighbors(current_node,None)
                for neighbour in neighbours:
                    if tuple(map(tuple, neighbour.state)) not  in closed_set and tuple(map(tuple, neighbour.state)) not in other_set:
                        frontier.append(neighbour)
        return None,[]
def DFS(initial_state,goal_state):
    if(checkSolvable(initial_state,goal_state) == False):
        print('This puzzle is unsolvable!')
        return None,[]
    else:
        initial_node=PuzzleNode(initial_state,parent=None,move=None,cost=0,heuristic=None)
        frontier=[]
        frontier.append(initial_node)
        explored=[]
        closed_set=set()
        other_set=set()
        maxDepth=0
        while frontier:
            current_node=frontier.pop()
            other_set.add(tuple(map(tuple, current_node.state)))
            explored.append(current_node)
            if current_node.getDepth()>maxDepth:
                maxDepth=current_node.getDepth()
            if current_node.state == goal_state:
                path = []
                print(f'The current depth:{current_node.getDepth()}')
                while current_node != None:
                    path.append((current_node.state, current_node.move))
                    current_node=current_node.parent
                return path[::-1],arrayStates(explored),maxDepth
            else:
                closed_set.add(tuple(map(tuple, current_node.state)))
                neighbours=generate_neighbors(current_node,None)
                for neighbour in neighbours:
                    if tuple(map(tuple, neighbour.state)) not  in closed_set and tuple(map(tuple, neighbour.state)) not in other_set:
                        frontier.append(neighbour)
        return None,[]
def a_star(initial_state, goal_state,func):
    if(checkSolvable(initial_state,goal_state) == False):
        print('This puzzle is unsolvable!')
        return None,[]
    else:
        initial_node = PuzzleNode(initial_state, heuristic=func(initial_state, goal_state))
        goal_node = PuzzleNode(goal_state)
        open_set = [initial_node]
        closed_set = set()
        explored = []
        maxDepth=0
        while open_set:
            current_node = heapq.heappop(open_set)
            explored.append(current_node)
            if current_node.getDepth()>maxDepth:
                maxDepth=current_node.getDepth()
            if current_node.state == goal_state:
                # Goal state reached, reconstruct and return the solution path
                path = []
                print(f'The current depth:{current_node.getDepth()}')
                while current_node:
                    path.append((current_node.state, current_node.move))
                    current_node = current_node.parent
                return path[::-1],explored,maxDepth

            closed_set.add(tuple(map(tuple, current_node.state)))

            neighbors = generate_neighbors(current_node,func)
            for neighbor in neighbors:
                if tuple(map(tuple, neighbor.state)) not in closed_set:
                    heapq.heappush(open_set, neighbor)

        return None,explored  # No solution found
def read_puzzle_from_file(file_path):
    with open(file_path, 'r') as file:
        line = file.readline().strip()
        print(line)
        values = list(map(int, line.split(',')))
        size = int(len(values) ** 0.5)
        puzzle_state = [values[i:i+size] for i in range(0, len(values), size)]
        return puzzle_state
def print_puzzle_path(solution_path):
     for step, (state, move) in enumerate(solution_path):
        print(f"Move {step }:")
        for row in state:
            print(" ".join(map(str, row)))
        print()


# Read initial and goal states from files
initial_file_path = 'puzzle_input.txt'
goal_file_path = 'puzzle_goal.txt'

initial_state = read_puzzle_from_file(initial_file_path)
goal_state = read_puzzle_from_file(goal_file_path)

#solution_path,explored=DFS(initial_state, goal_state)






def draw_grid(canvas):
    # Draw horizontal lines
    canvas.create_line(10, 240, 710, 240, width=2, fill="black")
    canvas.create_line(10, 480, 710, 480, width=2, fill="black")

    # Draw vertical lines
    canvas.create_line(240, 10, 240, 710, width=2, fill="black")
    canvas.create_line(480, 10, 480, 710, width=2, fill="black")


def draw_cells(canvas, cell_values,pos):
    canvas.delete("all")
    draw_grid(canvas)
    print(cell_values)
    for i in range(3):
        for j in range(3):
            cell_value = cell_values[i][j]
            color='black'
            if cell_value==0:
                color='red'
            cell_center_x = (j * 240) + 120
            cell_center_y = (i * 240) + 120
            canvas.create_text(cell_center_x, cell_center_y, text=cell_value, font=("Arial", 100), fill=color)

cell_values_array = initial_state

def gui(moves):
    root = tk.Tk()
    root.title("8 puzzle")
    root.geometry("1080x720")
    root.configure(bg="lightgray")

    canvas = tk.Canvas(root, width=720, height=720, bg="white")

    time.sleep(1)
    flag=False
    for move1 in moves:

        draw_cells(canvas, move1[0],())
        canvas.pack()
        root.update()
        time.sleep(0.5)
    root.mainloop()

solution_path,explored,max=DFS(initial_state, goal_state)
print("search depth"+str(max))

print(f'The number of explored nodes is:{len(explored)}')
if(solution_path != None):
    gui(solution_path)
# Solve the puzzle
#solution_path,explored = a_star(initial_state, goal_state,eucledian_distance)


# Print initial state
print("Initial State:")
for row in initial_state:
    print(" ".join(map(str, row)))

# Print goal state
print("\nGoal State:")
for row in goal_state:
    print(" ".join(map(str, row)))
if(solution_path != None):
    print_puzzle_path(solution_path)

