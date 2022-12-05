#! /usr/bin/env python3
import sys
import os
import re

def usage():
    print("Usage: {} [INPUT FILE]".format(sys.argv[0]))
    print("After following the box stack rearrangement instructions (using the improved mover), which boxes are on top?\n")
    print("\t-h\tPrint this help message\n")

# Globals
# This is the line index for where the stack numbers are
# This is used to help parse the stacks
NUMBER_LINE_INDEX = 0
# These are the index positions where each stack is
STACK_POSITIONS = []

def getNumStacks(lines):
    global NUMBER_LINE_INDEX, STACK_POSITIONS
    for i in range(len(lines)):
        line = lines[i]
        x = re.search(r"^\s*(\d+\s*){3,}", line)
        if x:
            # Set globals
            NUMBER_LINE_INDEX = i
            positions = re.finditer(r"\d+", x.group())
            STACK_POSITIONS = [m.span()[0] for m in positions]

            num_stacks = len(x.group().split())
            return num_stacks

def main(input_file_name):
    input_file = open(input_file_name)
    lines = input_file.readlines()
    num_stacks = getNumStacks(lines)

    stack_lines = lines[:NUMBER_LINE_INDEX]

    stacks = [[] for i in range(num_stacks)]
    for i in range(len(stack_lines), 0, -1):
        stack_idx = 0
        line = stack_lines[i - 1]
        for pos in STACK_POSITIONS:
            if line[pos].isalpha():
                stacks[stack_idx].append(line[pos])
            stack_idx += 1

    # Parse the move instructions
    instruction_lines = lines[NUMBER_LINE_INDEX + 1:]
    for line in instruction_lines:
        x = re.search(r"move\s+(\d+)\s+from\s+(\d+)\s+to\s+(\d+)", line)
        if x:
            instr = [int(v) for v in x.groups()]
            # -1 needed for index offset (stack #1 is index 0)
            amt, ifrom, ito = instr[0], instr[1] - 1, instr[2] - 1
            from_pile = [stacks[ifrom].pop() for i in range(amt)]
            # Reversing the pop'ed stack since the new mover picks up all boxes at once, so order is reversed
            stacks[ito] += from_pile[::-1]

    top_boxes = [s[-1] for s in stacks]
    print("The top boxes of each stack have the letters: {}".format(''.join(top_boxes)))

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