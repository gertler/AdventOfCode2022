#! /usr/bin/env python3
import sys
import os
from math import sqrt

def usage():
    print("Usage: {} [INPUT FILE]".format(sys.argv[0]))
    print("Find how many positions the tail of the rope visits for the new long rope.\n")
    print("\t-h\tPrint this help message\n")


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __eq__(self, __o: object) -> bool:
        return self.x == __o.x and self.y == __o.y
    
    def __hash__(self) -> int:
         return hash((self.x, self.y))
    
    def euclideanDistanceTo(self, point: object):
        x_diff = (self.x - point.x) ** 2
        y_diff = (self.y - point.y) ** 2
        return sqrt(x_diff + y_diff)
    
    def taxiDirectionsTo(self, point: object):
        return [point.x - self.x, point.y - self.y]
    
    def shiftedBy(self, x_off, y_off):
        new = Point(self.x + x_off, self.y + y_off)
        return new
    

def findTailPosFrom(head: Point, currTail: Point):
    if head == currTail:
        return currTail
    if head.euclideanDistanceTo(currTail) < 2:
        return currTail
    
    directions = currTail.taxiDirectionsTo(head)
    x, y = map(lambda x: 0 if x == 0 else x/abs(x), directions)
    return Point(currTail.x + x, currTail.y + y)


def main(input_file_name):
    input_file = open(input_file_name)
    lines = input_file.readlines()
    num_positions_visited = 0
    positions_visited = set() # add()

    currTail = Point(0,0)
    rope_length = 10
    # Head is rope[0]
    rope = [Point(0,0) for i in range(rope_length)]

    for line in lines:
        instr = line.split()
        x_diff = 0
        y_diff = 0
        if instr[0] == "U":
                y_diff = 1
        elif instr[0] == "D":
                y_diff = -1
        elif instr[0] == "L":
                x_diff = -1
        elif instr[0] == "R":
                x_diff = 1
        
        for i in range(int(instr[1])):
            rope[0] = rope[0].shiftedBy(x_diff, y_diff)
            # Move each knot of the rope 1 by 1
            for j in range(1, len(rope)):
                rope[j] = findTailPosFrom(rope[j - 1], rope[j])
            positions_visited.add(rope[-1])

    num_positions_visited = len(positions_visited)
    # for pos in positions_visited:
    #     print("({}, {})".format(pos.x, pos.y))
    print("The number of positions visited by the rope tail is {}".format(num_positions_visited))

    input_file.close()

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