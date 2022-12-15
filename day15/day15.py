#! /usr/bin/env python3
import sys
import os
import re

# Globals
Y_ROW = 2_000_000


class Sensor:
    def __init__(self, pos, taxi_radius):
        self.pos = pos
        self.taxi_radius = taxi_radius


def usage():
    print("Usage: {} [INPUT FILE]".format(sys.argv[0]))
    print("Find how many positions in row y={} that cannot contain a beacon.\n".format(Y_ROW))
    print("\t-h\tPrint this help message\n")


def taxiDistance(p1, p2):
    x_diff = abs(p1[0] - p2[0])
    y_diff = abs(p1[1] - p2[1])
    return x_diff + y_diff

def main(input_file_name):
    input_file = open(input_file_name)
    lines = input_file.readlines()
    input_file.close()

    num_without_beacon = 0

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

    # Using list of sensors, check each sensor and add to set() of positions where no beacon is (assuming y=Y_ROW)
    no_possible_beacons = set()
    for sensor in sensors:
        pos = sensor.pos
        dist_2_y_row = abs(pos[1] - Y_ROW)
        # Ignore sensors that are too far to care about Y_ROW
        if dist_2_y_row > sensor.taxi_radius:
            continue
        x_delta = sensor.taxi_radius - dist_2_y_row
        x_max = pos[0] + (sensor.taxi_radius - dist_2_y_row)
        for x in range(pos[0] - x_delta, pos[0] + x_delta + 1):
            no_possible_beacons.add((x, Y_ROW))

    
    # Finally, take set() of positions, and remove all positions where a beacon exists
    # This is done, because in the prior step, we assume ALL positions in taxi radius are no-beacon, not all minus 1
    for beacon in beacons:
        if beacon in no_possible_beacons:
            no_possible_beacons.remove(beacon)

    num_without_beacon = len(no_possible_beacons)
    print("In the row where y=2000000, {} positions cannot contain a beacon".format(num_without_beacon))

    

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