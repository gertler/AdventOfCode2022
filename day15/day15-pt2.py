#! /usr/bin/env python3
import sys
import os
import re
from itertools import filterfalse, tee
import time

# Globals
# 4_000_000
XY_MAX = 20
XY_MIN = 0

class Sensor:
    def __init__(self, pos, taxi_radius):
        self.pos = pos
        self.taxi_radius = taxi_radius


def usage():
    print("Usage: {} [INPUT FILE]".format(sys.argv[0]))
    print("Find the tuning frequency by finding the distress beacon coordinates.\n")
    print("\t-h\tPrint this help message\n")


def taxiDistance(p1, p2):
    x_diff = abs(p1[0] - p2[0])
    y_diff = abs(p1[1] - p2[1])
    return x_diff + y_diff

def main(input_file_name):
    input_file = open(input_file_name)
    lines = input_file.readlines()
    input_file.close()

    distress_beacon = (-1,-1)

    # Create list of sensors and beacons
    sensors = []
    beacons = []
    for line in lines:
        rgx = re.search(r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)", line)
        x, y, beacon_x, beacon_y = map(int, rgx.groups())
        sensor, beacon = [(x,y), (beacon_x,beacon_y)]
        taxi = taxiDistance(sensor, beacon)
        beacons.append(beacon)
        sensors.append(Sensor(sensor, taxi))

    # Next, loop over every row
    for y in range(0, XY_MAX + 1):
        print(f"Checking y={y}")
        curr_range = range(XY_MIN, XY_MAX + 1)
        # curr_range = filterfalse(lambda x: False, curr_range)
        for sensor in sensors:
            dist_2_y_row = abs(sensor.pos[1] - y)
            # Ignore sensors that are too far to care about current row
            if dist_2_y_row > sensor.taxi_radius:
                continue
            x_delta = sensor.taxi_radius - dist_2_y_row
            x_min, x_max = (sensor.pos[0] - x_delta, sensor.pos[0] + x_delta)

            before = time.time()
            new_range = filterfalse(lambda x: x_min <= x <= x_max, curr_range)
            # _, curr_range = tee(temp)
            after = time.time()
            # print(f"Took {after - before} seconds")
            # curr_range = new_range
            _new_range, curr_range = tee(new_range)
            # before = time.time()
            list(_new_range)
            # after = time.time()
            # print(f"Took {after - before} seconds")
            # curr_range = new_range
        
        found_x = list(curr_range)
        if len(found_x) > 0:
            distress_beacon = (found_x[0], y)
            break

    tuning_frequency = distress_beacon[0] * XY_MAX + distress_beacon[1]
    print("The tuning frequency is {}.".format(tuning_frequency))

    

if __name__ == "__main__":
    # Check args:
    if len(sys.argv) != 2:
        usage()
        exit(1)
    if sys.argv[1] == "-h":
        usage()
        exit(0)
    if not os.path.isfile(sys.argv[1]):
        usage()
        exit(1)
    main(sys.argv[1])