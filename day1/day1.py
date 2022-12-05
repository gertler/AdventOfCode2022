#! /usr/bin/env python3
import sys
import os

def usage():
    print("Usage: {} [INPUT FILE]".format(sys.argv[0]))
    print("Find the Elf carrying the most Calories.\n")
    print("\t-h\tPrint this help message\n")

def main(input_file_name):
    input_file = open(input_file_name)
    lines = input_file.readlines()
    current_most_calories = 0
    current_elf_carry_weight = 0
    for line in lines:
        if line.isspace():
            current_elf_carry_weight = 0
            continue
        weight = int(line)
        current_elf_carry_weight += weight
        if current_most_calories < current_elf_carry_weight:
            current_most_calories = current_elf_carry_weight
    
    print("The Elf carrying the most weight is carrying {} calories".format(current_most_calories))

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