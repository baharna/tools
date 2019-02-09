#!/usr/bin/python3

# Script to calculate hex value of a backward jump on the stack for shellcode execution

import argparse

def main(args):
    # Sets values for short jumps
    if int(args.jump) < 128:
        jump_bytes = int(args.jump) -1
        max_value = 255
    # sets values for near jumps
    else:
        jump_bytes = int(args.jump) -1
        max_value = 4294967295
    offset = hex(max_value - jump_bytes)
    print("The opcode to jump " + args.jump + " bytes is: " + offset)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-j', '--jump', required=True, help='number of bytes to jump back')
    args = parser.parse_args()
    if not args.jump.isdigit():
        parser.error("Jump bytes must be in int form")
    main(args)
