#! /usr/bin/env python3
import sys
import os

class Node:
    def __init__(self):
        self.altitude = 0
        self.neighbors = []
        self.isStart = False
        self.isDest = False
    
    def __str__(self) -> str:
        neighbors = ', '.join( map(lambda x: str(x.altitude), self.neighbors) )
        return "{} [{}]".format(self.altitude, neighbors)
    
    def setAltitude(self, altitude):
        if altitude == ord("S") or altitude == ord("a"):
            self.altitude = ord("a")
            self.isStart = True
        elif altitude == ord("E"):
            self.altitude = ord("z")
            self.isDest = True
        else:
            self.altitude = altitude

def usage():
    print("Usage: {} [INPUT FILE]".format(sys.argv[0]))
    print("Find the fewest steps required to move from all squares with elevation \"a\".\n")
    print("\t-h\tPrint this help message\n")


def find_shortest_path(graph, start, end):
    dist = { start: [start] }
    q = [start]
    while len(q) > 0:
        curr_node = q.pop(0)
        for next_node in curr_node.neighbors:
            if next_node not in dist.keys():
                dist[next_node] = [dist[curr_node], next_node]
                q.append(next_node)
    
    return dist.get(end)

def flattenNthArray(arrOrItem):
    if isinstance(arrOrItem, list):
        for item in arrOrItem:
            yield from flattenNthArray(item)
    else:
        yield arrOrItem

def main(input_file_name):
    input_file = open(input_file_name)
    lines = input_file.readlines()
    input_file.close()

    fewest_required_steps = 0

    # Set up graph with Node altitudes
    graph = []
    width = 0
    height = 0
    for line in lines:
        altitudes = [ord(c) for c in line.strip()]
        width = len(altitudes)
        height += 1
        for a in altitudes:
            n = Node()
            n.setAltitude(a)
            graph.append(n)
        
    # Create graph data structure
    def isWithinBounds(pos):
        return pos[0] in range(0, height) and pos[1] in range(0, width)
    for i in range(height):
        for j in range(width):
            flattened_idx = i * width + j
            node = graph[flattened_idx]

            deltas = [(1,0), (0,1), (-1,0), (0,-1)]
            # Up, Down, Left, & Right neighbors
            all_neighbors = [(i + d[0], j + d[1]) for d in deltas]
            # Filter out OOB neighbors
            real_neighbors = list(filter(isWithinBounds, all_neighbors))
            # Filter out neighbors that can't be reached (too steep)
            reachable_neighbors = list(filter(lambda t: node.altitude + 1 >= graph[t[0] * width + t[1]].altitude, real_neighbors))
            # Convert from list of coords to Nodes
            reachable_neighbor_nodes = list(map(lambda n: graph[n[0] * width + n[1]], reachable_neighbors))

            node.neighbors = reachable_neighbor_nodes
    
    # Find shortest path from starts to dest
    start_nodes = list(filter(lambda n: n.isStart, graph))
    dest_node = next(filter(lambda n: n.isDest, graph))
    path_lengths = []
    print("Checking {} nodes:".format(len(start_nodes)))
    for node in start_nodes:
        path = find_shortest_path(graph, node, dest_node)
        if not path:
            continue
        flattened_path = list(flattenNthArray(path))
        path_lengths.append(len(flattened_path) - 1)
    
    fewest_required_steps = sorted(path_lengths)[0]

    print("The fewest required steps is {}".format(fewest_required_steps))

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