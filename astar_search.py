from math import sqrt
from priorityQueue import PriorityQueue
class Node():

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

class AStar():
    """
    Class to perform A star search between two points in a 2 dimensional matrix
    """
    def __init__(self, grid):
        self.grid = grid
        self.to_sit = False

    def g_n(self, curr_node, start_node):
        curr_r, curr_c = curr_node
        start_r, start_c = start_node

        return sqrt((start_r - curr_r)**2 + (start_c -curr_c)**2)

    def f_n(self, curr_node, end_node):
        curr_r, curr_c = curr_node
        end_r, end_c = end_node

        return sqrt((end_r - curr_r)**2 +(end_c -curr_c)**2)

    def heuristic(self, a, b) -> float:
        # print(a, b)
        (x1, y1) = a
        (x2, y2) = b
        return abs(x1 - x2) + abs(y1 - y2)

    def a_star_search(self, start, goal):
        frontier = PriorityQueue()
        frontier.put(start, 0)
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0
        while not frontier.empty():
            current_cost, current = frontier.get()
            # print("current: ", current)
            path = []
            if current == goal:
                cur_node = goal
                path.append(cur_node)
                while came_from[cur_node] != None:
                    path.append(came_from[cur_node])
                    cur_node = came_from[cur_node]
                break
            
            for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                next = (current[0] + new_position[0], current[1]+ new_position[1])
                # Make sure within range
                # print("next: ", next)
                if next[0] > (len(self.grid) - 1) or next[0] < 0 or next[1] > (len(self.grid[len(self.grid)-1]) -1) or next[1] < 0:
                    continue

                if self.grid[next[0]][next[1]] in (-1,1,4,5) and next!= goal:
                    continue

                # Make sure walkable terrain
                # if not to_sit and self.grid[next[0]][next[1]] not in (0,2, id) or to_sit and self.grid[next[0]][next[1]] not in (0,2, 7,id) and next != goal:
                #     continue

                new_cost = cost_so_far[current] + 1
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + self.heuristic(next, goal)
                    frontier.put(next, priority)
                    came_from[next] = current
        
        path.reverse()
        return path

    def search(self, start, end):
        start_node = Node(None, start)
        start_node.g = start_node.h = start_node.f = 0
        end_node = Node(None, end)
        end_node.g = end_node.h = end_node.f = 0

        # Initialize both open and closed list
        open_list = []
        closed_list = []

        # Add the start node
        open_list.append(start_node)

        # Loop until you find the end
        while len(open_list) > 0:

            # Get the current node
            current_node = open_list[0]
            
            current_index = 0
            for index, item in enumerate(open_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index
            print(current_node.position)
            # Pop current off open list, add to closed list
            open_list.pop(current_index)
            closed_list.append(current_node)

            # Found the goal
            if current_node == end_node:
                path = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                return path[::-1] # Return reversed path

            # Generate children
            children = []
            for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares

                # Get node position
                node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

                # Make sure within range
                if node_position[0] > (len(self.grid) - 1) or node_position[0] < 0 or node_position[1] > (len(self.grid[len(self.grid)-1]) -1) or node_position[1] < 0:
                    continue

                # Make sure walkable terrain
                if self.grid[node_position[0]][node_position[1]] != 0:
                    continue

                # Create new node
                new_node = Node(current_node, node_position)

                # Append
                children.append(new_node)

            
            # Loop through children
            for child in children:
                print("children: ", child.position)
                # Child is on the closed list
                for closed_child in closed_list:
                    if child == closed_child:
                        continue

                # Create the f, g, and h values
                child.g = current_node.g + 1
                child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
                child.f = child.g + child.h

                # Child is already in the open list
                for open_node in open_list:
                    if child == open_node and child.g > open_node.g:
                        continue

                # Add the child to the open list
                open_list.append(child)

if __name__ == "__main__":
    maze = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    
    start = (1,1)
    end = (7,6)
    astar = AStar(maze)

    path = astar.search(start, end)
    
    print(path)
    print(astar.a_star_search(start,end)[2])