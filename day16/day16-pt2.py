#! /usr/bin/env python3
import sys
import os
import re
import math

# Globals
PART2 = False
TEST_MODE = False
MINUTES_ALLOWED = 26
START_VALVE = "AA"
TIME_2_MOVE = 1
TIME_2_OPEN = 1

class Valve:
    def __init__(self, name, flow_rate: int, connection_str):
        self.name = name
        self.flow_rate = flow_rate    
        self.connection_str = connection_str
        self.open = False
    
    def setLeadsTo(self, connections):
        self.connections = connections
    
    def getPotential(self, time_elapsed: int):
        if self.open:
            return 0
        time_remaining = MINUTES_ALLOWED - time_elapsed - TIME_2_OPEN
        if time_remaining <= 0:
            return 0
        return self.flow_rate * time_remaining

class Path:
    def __init__(self, potential: int, path: list):
        self.potential = potential
        self.path = path

def usage():
    print("Usage: {} [INPUT FILE]".format(sys.argv[0]))
    print("With an elephant helping, find the most pressure that can be released going through the tunnels.\n")
    print("\t-h\tPrint this help message\n")


def floyd_warshall(valves, distances):
    valve_names = valves.keys()
    for k in valve_names:
        for i in valve_names:
            for j in valve_names:
                if distances[i][j] > distances[i][k] + distances[k][j]:
                    distances[i][j] = distances[i][k] + distances[k][j]


def findBestPath(valves, distances):
    start = valves[START_VALVE]
    nonzero_valves = [v for _,v in valves.items() if v.flow_rate > 0]

    def _findBestPathRecursive(curr_valve: Valve, curr_potential: int, possible_next_valves: list, time_elapsed: int, path_2_here: list):
        if time_elapsed >= MINUTES_ALLOWED:
            return curr_potential
        potential = curr_valve.getPotential(time_elapsed)
        if time_elapsed > 0 and potential == 0:
            return curr_potential
        # path_potentials = [potential + curr_potential]

        paths = [Path(potential + curr_potential, path_2_here + [curr_valve])]
        pnv_sorted = sorted(possible_next_valves, key=lambda v: distances[curr_valve.name][v.name])
        for next_valve in pnv_sorted:
            dist = distances[curr_valve.name][next_valve.name]
            new_nonzero_valves = list(filter(lambda v: v != next_valve, pnv_sorted))
            new_time_elapsed = time_elapsed + dist + TIME_2_OPEN
            path_potential = _findBestPathRecursive(next_valve, potential + curr_potential, new_nonzero_valves, new_time_elapsed)
            path_potentials.append(path_potential)
        return max(path_potentials)

    potential = _findBestPathRecursive(start, 0, nonzero_valves, -TIME_2_OPEN, [])
    return potential
    

def main(input_file_name):
    input_file = open(input_file_name)
    lines = input_file.readlines()
    input_file.close()

    # First iteration parse lines
    rgx_str = r"^Valve ([A-Z]{2}) has flow rate=(\d+); tunnels? leads? to valves? (.+$)"
    valves = {}
    for line in lines:
        rgx = re.search(rgx_str, line)
        valve, flow, leads_to = rgx.groups()
        valves[valve] = Valve(valve, int(flow), leads_to)
    
    # Set tunnel connections
    distances = {}
    valve_keys = valves.keys()
    for _, valve in valves.items():
        connections = valve.connection_str.split(", ")
        connections = list(map(lambda x: valves[x], connections))
        valve.setLeadsTo(connections)
        distances[valve.name] = {k: math.inf for k in valve_keys}
        distances[valve.name][valve.name] = 0
        for conn in connections:
            distances[valve.name][conn.name] = TIME_2_MOVE

    # Traverse through the tunnels!
    # We really only care about reaching valves with non-zero flow rates
    floyd_warshall(valves, distances)

    most_pressure = findBestPath(valves, distances)
    print(f"The most pressure you can release is {most_pressure}")


if __name__ == "__main__":
    # Check args:
    if len(sys.argv) < 2:
        usage()
        exit(2)
    if sys.argv[1] == "-h":
        usage()
        exit(0)
    if len(sys.argv) >= 3 and sys.argv[2] == "-p2":
        PART2 = True
    if "-test" in sys.argv:
        TEST_MODE = True
    if not os.path.isfile(sys.argv[1]):
        usage()
        exit(1)
    main(sys.argv[1])