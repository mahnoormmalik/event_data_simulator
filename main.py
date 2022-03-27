import threading
import logging
import time
import random

from carnival import Carnival
from venue  import Venue

random.seed(40)
def add_some_values(grid, thread_name, row, col):
    logging.info("Thread %s: starting", thread_name)
    grid[row][col] = thread_name
    time.sleep(2)
    logging.info("Thread %s: finishing", thread_name)

if __name__ == "__main__":

    # Create and initialise venue for the event
    venue = Venue()
    venue.create_venue()
    carn = Carnival(venue)

    # carn.initialise_venue(50, 30, 2)

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    threads = list()
    carn.venue.print_venue()
    total_time = 1
    attendee_index = 0
    # threads = list()
    time = 0
    carn.simulate(4*60*60, 100)
    # while time < total_time and attendee_index< len(carn.attendees):
    #     print("here")
    #     attendee = carn.attendees[attendee_index]
    #     attendee.simulate_to_table(carn.venue.venue_grid, carn.venue.eating_areas, carn.entrance, time, 9)
    #     time += 1

    carn.venue.print_venue()
