#! /usr/bin/env python3
import sys
import os
import pprint

def usage():
    print("Usage: {} [INPUT FILE]".format(sys.argv[0]))
    print("Find how many trees are visible from outside the grid.\n")
    print("\t-h\tPrint this help message\n")


def calculateTreeVisabilityAndScenicScore(grid, vis_grid):

    def findScore(height, trees, direction):
        score = 0
        ts = trees[::-1] if direction == -1 else trees
        for tree in ts:
            score += 1
            if height <= tree:
                return score
        return score

    # Horizontal
    idx = 0

    for line in grid:
        # Forwards
        for i in range(1, len(line)):
            vis_grid[idx][i] *= findScore(line[i], line[:i], -1)
            
        # Backwards
        for j in range(len(line) - 2, 0, -1):
            vis_grid[idx][j] *= findScore(line[j], line[j+1:], 1)
        
        idx += 1


def main(input_file_name):
    input_file = open(input_file_name)
    lines = input_file.readlines()
    num_trees_visible = 0
    tree_grid = []
    x_len = 0
    for line in lines:
        heights = [int(x) for x in line.strip()]
        x_len = len(heights)
        tree_grid.append(heights)
    
    # In order to not double-count, we will start with a second grid of all False (assume not visible)
    # We will iterate through the grid horizontally AND vertically, forwards and backwards
    # Each time, we check the outside (in that direction) current tallest; if curr > curr_tallest, mark as visible

    # Visible grid with 1's around perimeter
    vis_grid = [[1]*x_len for i in range(len(tree_grid))]
    vis_grid[0] = [0]*x_len
    vis_grid[-1] = [0]*x_len
    for line in vis_grid:
        line[0] = 0
        line[-1] = 0
    
    # Horizontal
    calculateTreeVisabilityAndScenicScore(tree_grid, vis_grid)

    # Rotate grid using magic; output has lines as tuples
    rotated_grid = list(zip(*tree_grid[::-1]))
    # Convert tuples to lists
    rotated_grid = [[i for i in l][::-1] for l in rotated_grid]
    rotated_vis = list(zip(*vis_grid[::-1]))
    rotated_vis = [[i for i in l][::-1] for l in rotated_vis]

     # Vertical
    calculateTreeVisabilityAndScenicScore(rotated_grid, rotated_vis)
    
    num_trees_visible = max([max(l) for l in rotated_vis])
    
    print("The highest scenic score is {} ".format(num_trees_visible))

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