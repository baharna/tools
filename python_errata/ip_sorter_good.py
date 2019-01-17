#!/usr/bin/python3

import struct
import socket

ips = ["192.168.1.1", "11.11.13.10", "192.168.5.6", "200.5.13.200", "10.10.10.1", "127.0.0.1","200.5.13.1", "213.125.123.100", "88.11.88.11"]
sorted_ips = []

def convert_to_ip(x):
    reg_ip = socket.inet_ntoa(struct.pack("!L", x))
    return reg_ip

def convert_to_long(ip):
    long_ip = struct.unpack("!L", socket.inet_aton(ip))[0]
    return long_ip

def main():
    for x in ips:
        sorted_ips.append(convert_to_long(x))
    list.sort(sorted_ips)
    for x in sorted_ips:
        sorted_ips[sorted_ips.index(x)] = convert_to_ip(x)
    for item in sorted_ips:
        print(item)

if __name__ == '__main__':
    main()
