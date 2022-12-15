#! /usr/bin/env python3
import sys
import os
import re
import time

# Globals
# 4_000_000
XY_MAX = 4_000_000
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


def find_gap_with_size(ranges, gap):
    s = sorted(ranges, key=lambda x: x[0])
    # Quick check if gap exists at beginning
    if s[0][0] == XY_MIN + 1:
        return (True, XY_MIN)

    max_x = s[0][1]
    for i in range(1, len(s)):
        if s[i][0] == max_x + gap + 1:
            return (True, max_x + 1)
        if s[i][1] < max_x:
            continue
        max_x = s[i][1]
    
    # Quick check if gap exists at end
    if max_x == XY_MAX - 1:
        return (True, XY_MAX)
    return (False, -1)

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

    before = time.time()
    # Next, loop over every row
    for y in range(0, XY_MAX + 1):
        if y % 250_000 == 0:
            print(f"Checking y={y}...")
        # Grab the list of ranges for the covered cells by each sensor on the current row
        curr_ranges = []
        for sensor in sensors:
            dist_2_y_row = abs(sensor.pos[1] - y)
            # Ignore sensors that are too far to care about current row
            if dist_2_y_row > sensor.taxi_radius:
                continue
            x_delta = sensor.taxi_radius - dist_2_y_row
            x_min, x_max = (sensor.pos[0] - x_delta, sensor.pos[0] + x_delta)
            curr_ranges.append((x_min, x_max))
        
        # Check if there is a gap of size 1 within the covered cells
        # If so, that must be our distress beacon
        if len(curr_ranges) < 2:
            continue
        found_gap, gap = find_gap_with_size(curr_ranges, 1)
        if found_gap:
            distress_beacon = (gap, y)
            break
    
    after = time.time()
    print(f"Took {after - before} seconds")
    print(f"Distress beacon is at {distress_beacon}")
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