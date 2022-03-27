from random import choice, choices, seed, randrange
from time import time
from astar_search import AStar
import heapq
import pandas as pd

seed(10)


class Attendee():
    def __init__(self, id, arrival_time, time_spent, entrance):
        self.id = id
        self.arrival_time = arrival_time
        self.time_spent = time_spent
        self.party_size = 0
        self.party_members = []
        self.stalls_to_visit = []
        self.time = 0
        self.f = open("data/logs_" +str(self.id) +".csv","w" )
        self.f.write("id,row,col,time, time_delta(s) \n")
        self.current_pos = entrance

    def simulate(self, venue_grid, stalls, sitting_area, entrance, time):
        print("*" * 10)
        print("simulating graph for attendee %d" %(self.id))
        current_pos= entrance
        stall_to_visit= choice(stalls)
        
        astar = AStar(venue_grid)
        self.time = time
        print("Arrival_time: %d" %(self.arrival_time))
        sit_or_stall = "sit"
        path = []
        while self.time - self.arrival_time < self.time_spent:
            # print("Current_time: ", self.time)
            # print("Remaining time: ", self.arrival_time + self.time_spent)
            if sit_or_stall == "sit":
                # do not sit again
                sit_or_stall = "stall"
            else:
                sit_or_stall = choices(["sit", "stall"], weights=(30, 70), k=1)[0]
            if sit_or_stall == "stall":
                # print("going to stall")
                while current_pos == stall_to_visit.entrance:
                    stall_to_visit = choice(stalls)
                path.extend(astar.a_star_search(current_pos, stall_to_visit.entrance, False, self.id))
                wait_time = int(randrange(0,10,1))
                self.add_wait_time(path, wait_time)
                if not path:
                    print("no path to stall from ", current_pos, " to ", stall_to_visit.entrance)
                current_pos = stall_to_visit.entrance
            else:
                # print("going to sit")
                _, table = heapq.heappop(sitting_area)
                path.extend(astar.a_star_search(current_pos, table.seats[0], True, self.id))
                wait_time = int(randrange(10,20,1))
                self.add_wait_time(path, wait_time)
                if not path:
                    print("no path to table from ", current_pos, " to ", table.seats[0])
                current_pos = table.seats[0]
                heapq.heappush(sitting_area, (0, table))
            self.add_path_to_venue(path, venue_grid)
        # print(stall_to_visit)

    def add_wait_time(self, path, wait_time):
        sit_pos = path[-1]
        # print("going to wait")
        for i in range(wait_time * 60):
            path.append(sit_pos)

        # self.time += wait_time * 60

    def add_path_to_venue(self, path, venue_grid):
        # print(path)
        
        for i, p in enumerate(path):
            r,c = p[0], p[1]
            time_stamp = pd.to_datetime(self.time, unit='s', origin=pd.Timestamp('2022-01-30 15:00:00'))
            self.f.write(str(r)+ "," + str(c)+"," + str(time_stamp)+ "," + str(self.time) + "\n")
            venue_grid[r][c] = self.id
            self.time += 1

    def __del__(self):
        self.f.close()