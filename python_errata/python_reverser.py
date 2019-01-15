#!/usr/bin/python3

# Script to reverse strings and commands and output as hex for the purpose of 
# inputting into shellcode

import argparse

# print formatted reversed string when divisible by 4
def string_printer(printer_string):
    max = len(printer_string) // 4
    count = 0
    while count < max:
        print(printer_string[count*4:(count+1)*4] + ":\t" + printer_string[count*4:(count+1)*4].encode('utf-8').hex())
        count += 1

def main(args):
    # Take string, print it in original, reversed, and hex form
    string = args.string
    reversed_string = string[::-1]
    hex_string = reversed_string.encode('utf-8').hex()
    print("String Length: " + str(len(reversed_string)))
    print("Original String: " + string)
    print("Reversed String: " + reversed_string)
    print("Hexed Reversed String: " + hex_string)
    # if string length is directly divisible by 4, proceed to printer
    if len(string) % 4 == 0:    
        string_printer(reversed_string)
    # if string is NOT directly divisible by 4, break off the remainder and print it
    else:
        # Warning to consider padding teh shellcode to make it divisible by 4, help control null bytes
        print("**Warning: string not divisible by 4, manually check to ensure it does not cause issues with shellcode**")
        # Take the modulo of the string, format and print it
        leftovers = len(reversed_string) % 4
        leftover_string = ""
        for item in reversed_string[0:leftovers]:
            leftover_string += item
        print(leftover_string + ":\t" + leftover_string.encode('utf-8').hex())
        # Send the remaining string portion to the printer
        remaining_string = reversed_string[leftovers:len(reversed_string)]
        string_printer(remaining_string)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # require -s switch for the string to be formatted
    parser.add_argument('-s', '--string', required=True, help='String or command to reverse')
    args = parser.parse_args()
    main(args)
