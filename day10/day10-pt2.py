#! /usr/bin/env python3
import sys
import os

# Globals
ADDX_INSTR_CYCLES = 2

def usage():
    print("Usage: {} [INPUT FILE]".format(sys.argv[0]))
    print("Find the sum of signal strengths.\n")
    print("\t-h\tPrint this help message\n")

def main(input_file_name):
    input_file = open(input_file_name)
    lines = input_file.readlines()
    input_file.close()

    buf = []
    x_reg = 1
    output = ""

    cycle_idx = 1
    line_idx = 0
    while line_idx < len(lines):
        print("During cycle #{}: X is {}".format(cycle_idx, x_reg))
        line = lines[line_idx]

        draw_ptr = (cycle_idx - 1) % 40
        if draw_ptr in range(x_reg - 1, x_reg + 2):
            output += "#"
        else:
            output += "."
        if (cycle_idx) % 40 == 0:
            output += "\n"
        
        cycle_idx += 1
        
        new_val = 0
        if "noop" in line:
            line_idx += 1
            continue
        elif "addx" in line:
            _, new_val = line.split()
        
        if len(buf) == 0:
            buf = [int(new_val)] + [0] * (ADDX_INSTR_CYCLES - 1)
        
        x_reg += buf.pop()
        if len(buf) == 0:
            line_idx += 1
    
    # Correct answer is RGZEHURK
    print("Output:\n{}".format(output))

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