#! /usr/bin/env python3
import sys
import os

def usage():
    print("Usage: {} [INPUT FILE]".format(sys.argv[0]))
    print("Finds the item type that corresponds to each Elf group's badge and sums their priorities.\n")
    print("\t-h\tPrint this help message\n")

def main(input_file_name):
    input_file = open(input_file_name)
    lines = input_file.readlines()
    priority_sum = 0
    g1, g2, g3 = (lines[::3], lines[1::3], lines[2::3])
    groups = list(zip(g1, g2, g3))

    for group in groups:
        # Intersection of 3 Elves in the group
        shared_item = set(group[0].strip()).intersection(set(group[1].strip()))
        shared_item = shared_item.intersection(set(group[2].strip()))
        shared_item = list(shared_item)[0]
        if shared_item.islower():
            priority_sum += ord(shared_item) - 96
        else:
            priority_sum += ord(shared_item) - 38
        
    print("The sum of priorities for each group badge item is {} ".format(priority_sum))

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