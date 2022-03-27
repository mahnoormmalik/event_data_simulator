from collections import deque
from random import choice
import heapq

class Venue():
    def __init__(self, width = 50, height = 30, stall_width=3, stall_height=3):
        self.num_stalls = 0
        self.eating_areas = []
        self.rows = width * 2
        self.columns = height * 2
        self.venue_grid = []
        self.stalls = []
        self.sitting_area_height = 30
        self.sitting_area_width = 20
        self.stall_width = stall_width
        self.stall_height = stall_height
        self.entrance = (self.rows - 1, self.columns - 9)
        self.exit = (0, self.columns - 9)

    def create_venue(self):
        self.venue_grid = [[0] * self.columns for i in range(self.rows)]
        self.create_stalls(self.stall_width * 2, self.stall_height * 2)

        self.create_sitting_area()
        self.create_entrance(self.entrance, 3)

    def create_stalls(self, width, height):
        for col in range(self.columns):
            self.venue_grid[0][col] = -1
            self.venue_grid[self.rows-1][col] = -1

        for row in range(self.rows):
            self.venue_grid[row][0] = -1
            self.venue_grid[row][self.columns - 1] = -1

        #create left vertical stalls
        id = 0
        row = 1
        while row < self.rows - (height + 1):

            stall = Stall(id,"Pakistani" ,width, height, 10, (row + 1, width + 1))
            self.venue_grid[row + 1][width + 1] = 2
            self.stalls.append(stall)
            self.create_stall_on_grid(row, 1, width, height)
            row += height + 1

        #create right vertical stalls
        row = 5
        while row < self.rows - (height + 1):
            stall = Stall(id,"Pakistani" ,width, height, 10, (row + 1, self.columns - width - 2))
            self.venue_grid[row + 1][self.columns - width - 2] = 2
            self.stalls.append(stall)
            self.create_stall_on_grid(row, self.columns - width - 1, width, height)
            row += height + 1

        #create top horizontal stalls
        col = 1 + width + 2

        while col < self.columns - 2*(width + 1):
            stall = Stall(id,"Pakistani" ,width, height, 10, (height + 1, col + 1))
            self.venue_grid[height + 1][col + 1] = 2
            self.stalls.append(stall)
            self.create_stall_on_grid(1, col, width, height)
            col += width + 1

        #create bottom horizontal stalls
        col = 1 + width + 2

        while col < self.columns - 2*(width + 1):
            stall = Stall(id,"Mexican" ,width, height, 10, (self.rows - height - 2, col + 1))
            self.venue_grid[self.rows - height - 2][col + 1] = 2
            self.stalls.append(stall)
            self.create_stall_on_grid(self.rows - height - 1, col, width, height)
            col += width + 1
    
    def create_sitting_area(self):
        start_row = (self.rows - self.sitting_area_height) // 2
        start_col = (self.columns - self.sitting_area_width) // 2

        sits = choice([2,6])
        # print(start_row, start_col)
        curr_row = start_row
        while curr_row < start_row + self.sitting_area_height:
            curr_col = start_col
            while curr_col < start_col + self.sitting_area_width:

                """
                TODO: create an object of sitting area class and add to the self.eating_area queue
                """
                # sits = choice([2,6])
                sits = 2
                if sits == 2:
                    # chair = 4, table = 5, sitting area = 7
                    sitting_area = Sitting_Area(sits, False, [], [(curr_row, curr_col), (curr_row + 2, curr_col)])
                    
                    heapq.heappush(self.eating_areas, (0, sitting_area))
                    self.venue_grid[curr_row][curr_col] = 4
                    self.venue_grid[curr_row+1][curr_col] = 5
                    self.venue_grid[curr_row+2][curr_col] = 4
                    
                    self.venue_grid[curr_row][curr_col+1] = 7
                    self.venue_grid[curr_row+1][curr_col+1] = 7
                    self.venue_grid[curr_row+2][curr_col+1] = 7
                    curr_col += 2
                else:
                    for row in range(3):
                        for col in range(3):
                            if row == 1:
                                self.venue_grid[curr_row + row][curr_col +col] = 5
                            else:
                                self.venue_grid[curr_row + row][curr_col +col] = 4
                        self.venue_grid[curr_row + row][curr_col + 3] = 7
                    curr_col += 4
            curr_row += 3
    
    def create_entrance(self, start, width):
        for c in range(width):
            self.venue_grid[start[0]][start[1] + c] = 0


    def create_stall_on_grid(self, row, col, width, height):
        """
        creates a width x height stall given the top left corners 
        of stall
        """
        for r in range(height):
            for c in range(width):
                self.venue_grid[row+r][col+c] = 1

    def print_venue(self):
        for row in range(self.rows):
            curr_row = []
            for col in range(self.columns):
                curr_row.append(self.venue_grid[row][col])
            print(curr_row)
               
class Sitting_Area():
    """
    Class to represent sitting areas on the venue

    Variables:
    sits-> int: number of people that can sit on the table
    is_occupied -> boolean: occupied or not
    attendess -> list(attendee): attendees seated at the place
    seats -> list(tuple(row,col)): the row, col of each seat in the sitting area
        
    """
    def __init__(self, sits, is_occupied, attendees, seats) -> None:
        
        self.sits = sits
        self.is_occupied = is_occupied
        self.attendees = attendees
        self.seats = seats
    
    def __eq__(self, sitting_area: object) -> bool:
        return self.is_occupied == sitting_area.is_occupied and self.sits == sitting_area.sits

    def __lt__(self, other):
        return self.is_occupied < other.is_occupied and self.sits < other.sits



class Stall():
    def __init__(self, id, cuisine, width, height, wait_time, entrance):
        self.id = id
        self.cuisine = cuisine
        self.width = width
        self.height = height
        self.queue = deque()
        self.wait_time = wait_time
        self.entrance = entrance

    def add_to_queue(self, attendee, current_time):
        self.queue.append((current_time, attendee))

if __name__ == "__main__":
    
    width = 50
    height = 30

    v = Venue()
    v.rows = width * 2 
    v.columns = height * 2

    v.venue_grid = [[0] * v.columns for i in range(v.rows)]
    # print(v.venue_grid)
    v.create_stalls(6,6)
    v.create_sitting_area()
    v.print_venue()

