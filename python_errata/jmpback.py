#!/usr/bin/python3

# Script to calculate hex value of a backward jump on the stack for shellcode execution

import argparse

def main(args):
    jump_bytes = int(args.jump) -1
    max_value = 255
    offset = hex(255 - jump_bytes)
    print("The hex value to jump " + args.jump + " bytes is: " + offset)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-j', '--jump', required=True, help='number of bytes to jump back')
    args = parser.parse_args()
    if not args.jump.isdigit():
        parser.error("Jump bytes must be in int form")
    main(args)
