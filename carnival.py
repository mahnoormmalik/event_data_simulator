from secrets import choice
import numpy as np
import threading
import logging
import heapq
import random
import pandas as pd
from attendee import Attendee
from venue import Venue
from astar_search import AStar


class Carnival():
    def __init__(self, venue):
        self.attendees = []
        self.STALL_WIDTH = 3
        self.STALL_HEIGHT = 3
        self.venue = venue
        self.carnival_state = {}
        self.event_time = 4 * 60 # minutes
        self.astar = AStar(self.venue.venue_grid)

    def create_attendees(self, num_attendees):
        mean = (self.event_time-30) / 2
        sigma = (mean * 1.341) - mean 
        arrival_times = np.random.normal(mean, sigma, 250).tolist()
        time_spent = np.random.normal(90, 20, 250)

        arrival_times.sort()

        for i in range(num_attendees):

            arrival_times[i] = abs(arrival_times[i])

            attendee = Attendee(i+8, int(arrival_times[i] * 60), int(time_spent[i] *60), self.venue.entrance)
            self.attendees.append(attendee)
            # attendee.simulate(self.venue.venue_grid, self.venue.stalls, self.entrance)


    def initialise_venue(self, width=50, height=30, num_attendees=1):
        """
        not needed anymore
        """
        self.venue.rows = width * 2 
        self.venue.columns = height * 2

        self.venue.venue_grid = [[0] * self.venue.columns for i in range(self.venue.rows)]

        self.venue.create_stalls(self.STALL_WIDTH * 2, self.STALL_HEIGHT * 2)

        self.venue.create_sitting_area()
        self.venue.create_entrance(self.entrance, 3)
        # self.venue.print_venue()

    def simulate(self, total_time, num_attendees=1):
        
        self.create_attendees(num_attendees)
        threads = list()
        print("Total event time: %s", total_time)

        for attendee in self.attendees:
            print("Attendee %d arrival_time: %d"  %(attendee.id, attendee.arrival_time))

            # x = threading.Thread(target=attendee.simulate, args=(self.venue.venue_grid, 
            #                     self.venue.stalls,self.venue.eating_areas, 
            #                     self.venue.entrance, time))
            x = threading.Thread(target=self.simulate_attendee, args=(attendee, 
                                attendee.arrival_time))
            threads.append(x)
            x.start()
            
        for index, thread in enumerate(threads):
            logging.info("Main    : before joining thread %d.", index)
            thread.join()
            logging.info("Main    : thread %d done", index)

    def adjust_path_to_speed(self, path):
        new_path = []
        i = 0
        while i < len(path):
            new_path.append(path[i])
            i+= 3

        return new_path

        
    def simulate_attendee(self, attendee, time):
        """
        TODO: Move simulate from attendee here
        """
        attendee.current_pos = self.venue.entrance
        stall_to_visit = choice(self.venue.stalls)

        sit_or_stall = "sit"
        path = []
        attendee.time = time
        while attendee.time - attendee.arrival_time < attendee.time_spent:
            if sit_or_stall == "sit":
                # do not sit again
                sit_or_stall = "stall"
            else:
                sit_or_stall = random.choices(["sit", "stall"], weights=(30, 70), k=1)[0]
            if sit_or_stall == "stall":
                while attendee.current_pos == stall_to_visit.entrance:
                    stall_to_visit = choice(self.venue.stalls)
                path.extend(self.adjust_path_to_speed(self.astar.a_star_search(attendee.current_pos, stall_to_visit.entrance)))
                wait_time = int(random.randrange(0,10,1))
                self.add_wait_time(path, wait_time)
                if not path:
                    print("no path to stall from ", attendee.current_pos, " to ", stall_to_visit.entrance)
                attendee.current_pos = stall_to_visit.entrance
            else:
                _, table = heapq.heappop(self.venue.eating_areas)
                path.extend(self.adjust_path_to_speed(self.astar.a_star_search(attendee.current_pos, table.seats[0])))
                wait_time = int(random.randrange(10,20,1))
                self.add_wait_time(path, wait_time)
                if not path:
                    print("no path to table from ", attendee.current_pos, " to ", table.seats[0])
                attendee.current_pos = table.seats[0]
                heapq.heappush(self.venue.eating_areas, (0, table))
            self.add_path_to_venue(path, attendee)

        self.simulate_exit(attendee)

    def simulate_exit(self, attendee):
        path = self.astar.a_star_search(attendee.current_pos, self.venue.exit)
        # print("exit path: ", path)
        self.add_path_to_venue(self.adjust_path_to_speed(path), attendee)
    
    def add_wait_time(self, path, wait_time):
        sit_pos = path[-1]
        # print("going to wait")
        for i in range(wait_time * 60):
            path.append(sit_pos)

    def add_path_to_venue(self, path, attendee):
        # print(path)
        
        for i, p in enumerate(path):
            r,c = p[0], p[1]
            time_stamp = pd.to_datetime(attendee.time, unit='s', origin=pd.Timestamp('2022-01-30 15:00:00'))
            attendee.f.write(str(attendee.id) + "," + str(r)+ "," + str(c)+"," + str(time_stamp)+ "," + str(attendee.time) + "\n")
            self.venue.venue_grid[r][c] = attendee.id
            attendee.time += 1

        

if __name__ == "__main__":
    carnival = Carnival()
    carnival.initialise_venue(50, 30)
    # carnival.simulate(240)
    carnival.venue.print_venue()


