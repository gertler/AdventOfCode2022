#! /usr/bin/env python3
import sys
import os

def usage():
    print("Usage: {} [INPUT FILE]".format(sys.argv[0]))
    print("Find how many Elf cleaning assignment pairs where the ranges overlap.\n")
    print("\t-h\tPrint this help message\n")

def main(input_file_name):
    input_file = open(input_file_name)
    lines = input_file.readlines()
    num_overlap_pairs = 0
    for line in lines:
        elf1, elf2 = line.split(',')
        elf1, elf2 = elf1.split('-'), elf2.split('-')
        elf1 = list(map(lambda x: int(x), elf1))
        elf2 = list(map(lambda x: int(x), elf2))
        # First entirely below second
        if elf1[1] < elf2[0]:
            continue
        # First entirely above second
        elif elf1[0] > elf2[1]:
            continue
        num_overlap_pairs += 1
    
    print("The number of assignment pairs where the ranges overlap is {}".format(num_overlap_pairs))

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