#! /usr/bin/env python3
import sys
import os

def usage():
    print("Usage: {} [INPUT FILE]".format(sys.argv[0]))
    print("Find how many Elf cleaning assignment pairs where one range fully contains the other.\n")
    print("\t-h\tPrint this help message\n")

def main(input_file_name):
    input_file = open(input_file_name)
    lines = input_file.readlines()
    num_hungry_pairs = 0
    for line in lines:
        elf1, elf2 = line.split(',')
        elf1, elf2 = elf1.split('-'), elf2.split('-')
        elf1 = list(map(lambda x: int(x), elf1))
        elf2 = list(map(lambda x: int(x), elf2))
        # First contains second
        if elf1[0] <= elf2[0] and elf1[1] >= elf2[1]:
            num_hungry_pairs += 1
        # Second contains first
        elif elf2[0] <= elf1[0] and elf2[1] >= elf1[1]:
            num_hungry_pairs += 1
    
    print("The number of assignment pairs where one range fully contains the other is {}".format(num_hungry_pairs))

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