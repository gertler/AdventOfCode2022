#! /usr/bin/env python3
import sys
import os
import pprint

# Globals
MAX_TRIES = 100_000

def usage():
    print("Usage: {} [INPUT FILE]".format(sys.argv[0]))
    print("Find the Elf carrying the most Calories.\n")
    print("\t-h\tPrint this help message\n")


def simulate_1_grain(formation, sand_start):
    def hasRock(pos):
        return formation[pos[1]][pos[0]]
    def putRock(pos):
        formation[pos[1]][pos[0]] = True
    atRest = False
    curr_pos = sand_start
    while not atRest:
        next_pos = (curr_pos[0], curr_pos[1] + 1)
        if not hasRock(next_pos):
            curr_pos = next_pos
            continue
        next_pos = (curr_pos[0] - 1, curr_pos[1] + 1)
        if not hasRock(next_pos):
            curr_pos = next_pos
            continue
        next_pos = (curr_pos[0] + 1, curr_pos[1] + 1)
        if not hasRock(next_pos):
            curr_pos = next_pos
            continue
        putRock(curr_pos)
        atRest = True


def simulate_sand(formation, sand_start):
    settled = 0
    curr_pos = sand_start
    for _ in range(MAX_TRIES):
        try:
            simulate_1_grain(formation, sand_start)
        except IndexError:
            return settled
        settled += 1
    
    return settled



def main(input_file_name):
    input_file = open(input_file_name)
    lines = input_file.readlines()
    input_file.close()

    # Parse the input
    restful_sand = 0
    rocks = []
    width = 0
    height = 0
    for line in lines:
        tokens = line.strip().split(' -> ')
        ray_strings = map(lambda x: x.split(','), tokens)
        rays = [(int(x), int(y)) for x,y in ray_strings]
        rocks.append(rays)
        _zipped = zip(*rays)
        max_x = max(next(_zipped))
        max_y = max(next(_zipped))
        if max_x > width:
            width = max_x
        if max_y > height:
            height = max_y

    # Add the rocks
    # [(503, 4), (502, 4), (502, 9), (494, 9)]
    # (503, 502), (4, 4)
    # (503, 501, -1), (4, 5, 1)
    formation = [[False]*(width + 1) for _ in range(height + 1)]
    for rays in rocks:
        for i in range(len(rays) - 1):
            x_diff, y_diff = zip(*rays[i:i+2])
            x_step = -1 if x_diff[0] > x_diff[1] else 1
            y_step = -1 if y_diff[0] > y_diff[1] else 1
            for x in range(x_diff[0], x_diff[1] + x_step, x_step):
                for y in range(y_diff[0], y_diff[1] + y_step, y_step):
                    formation[y][x] = True
    
    # Print rock wall
    # for l in formation:
    #     line = list(map(lambda x: "#" if x else ".", l))
    #     print(''.join(line))
    
    sand_start = (500, 0)
    restful_sand = simulate_sand(formation, sand_start)
    
    print("The number of units of sand that come to rest before it starts infinitely falling is {}".format(restful_sand))

    

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