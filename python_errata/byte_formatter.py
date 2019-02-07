#!/usr/bin/python3
#
# place bytes cut from debugger in here
# formats bytes for python script
shellcode = ""


formatted = ""

for x in shellcode.split(" "):
    y = x
    formatted += "\\x"
    formatted += y

print(formatted)
print("Len: %d" % len(shellcode))
