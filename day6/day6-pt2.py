#! /usr/bin/env python3
import sys
import os

def usage():
    print("Usage: {} [INPUT FILE]".format(sys.argv[0]))
    print("Determine how many characters need to be processed before the first start-of-packet marker is detected.\n")
    print("\t-h\tPrint this help message\n")

def main(input_file_name):
    input_file = open(input_file_name)
    line = input_file.readline()
    num_processed = 0
    num_unique = 14
    lastX = []
    for c in line:
        num_processed += 1
        if len(lastX) == num_unique:
            lastX = lastX[1:] + [c]
        else:
            lastX.append(c)
        
        if len(set(lastX)) == num_unique:
            break
    
    print("The number of characters processed before the start-of-packet marker is detected is {}".format(num_processed))

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