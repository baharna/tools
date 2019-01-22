#!/usr/bin/python3
# fix shellcode to get placed into createthread.asm


shellcode = b"<SHELLCODE>"
fixed = ""

for x in shellcode:
    fixed += '0x'
    fixed += '%02x,' % x

print(fixed)
