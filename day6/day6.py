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
    last4 = []
    for c in line:
        num_processed += 1
        if len(last4) == 4:
            last4 = last4[1:] + [c]
        else:
            last4.append(c)
        
        if len(set(last4)) == 4:
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