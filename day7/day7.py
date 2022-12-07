#! /usr/bin/env python3
import sys
import os
import re

# Globals
MAX_DIR_SIZE = 100_000

class Tree:
    def __init__(self):
        self.children = []
        self.name = None
        self.size = None
        self.parent = None
    
    def printRoot(self, padding):
        if len(self.children) == 0:
            print("{}{} (size={})".format(padding, self.name, self.size))
        else:
            print("{}{} (dir)".format(padding, self.name))
            for child in self.children:
                child.printRoot(padding + "|   ")
    
    def rootSize(self):
        if len(self.children) == 0:
            return self.size
        else:
            total = 0
            for child in self.children:
                total += child.rootSize()
            return total


def usage():
    print("Usage: {} [INPUT FILE]".format(sys.argv[0]))
    print("Finds the sum of the size of all directories that each have a max size of 100,000.\n")
    print("\t-h\tPrint this help message\n")


def getAllDirSizes(root: Tree):
    sizes = []
    sizes.append(root.rootSize())

    def getAllDirSizesRecur(rRoot: Tree):
        nonlocal sizes
        if len(rRoot.children) == 0:
            return
        sizes.append(rRoot.rootSize())
        for child in rRoot.children:
            getAllDirSizesRecur(child)
        

    for child in root.children:
        getAllDirSizesRecur(child)
    return sizes


def main(input_file_name):
    input_file = open(input_file_name)
    lines = input_file.readlines()

    dir_tree = Tree()
    dir_tree.name = "/"

    current_dir = dir_tree

    def change_dir(to):
        nonlocal current_dir
        if to == "..":
            current_dir = current_dir.parent
        elif to == "/":
            current_dir = dir_tree
        # Go to child
        else:
            exists = False
            for child in current_dir.children:
                if to == child.name:
                    current_dir = child
                    exists = True
            if not exists:
                new_child = Tree()
                new_child.parent = current_dir
                new_child.name = to
                current_dir.children.append(new_child)
                current_dir = new_child
    
    def parse_ls(tkn1, tkn2):
        nonlocal current_dir
        children_names = [c.name for c in current_dir.children]
        if tkn1 == "dir":
            if tkn2 not in children_names:
                new_child = Tree()
                new_child.parent = current_dir
                new_child.name = tkn2
                current_dir.children.append(new_child)
        # Parse single file
        else:
            if tkn2 not in children_names:
                new_child = Tree()
                new_child.parent = current_dir
                new_child.name = tkn2
                new_child.size = int(tkn1)
                current_dir.children.append(new_child)

    
    for line in lines:
        x = re.search(r"^\$\s+(\w+)(?=\s+([\w\.\/]+))?", line)
        # Not a command
        if not x:
            y = re.search(r"^(dir|\d+)\s+([\w\.]+)$", line)
            tokens = y.groups()
            parse_ls(tokens[0], tokens[1])
        # Is command
        else:
            tokens = x.groups()
            if tokens[0] == "cd":
                change_dir(tokens[1])
            elif tokens[0] == "ls":
                # Do nothing, just go to next line
                continue
    
    # dir_tree.printRoot("")

    total_size = 0
    sizes = getAllDirSizes(dir_tree)
    sizes_under = filter(lambda x: x <= MAX_DIR_SIZE, sizes)
    total_size = sum(sizes_under)

    print("The total size of all directories (including overlap) of a maximum size of {} is {}".format(MAX_DIR_SIZE, total_size))

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