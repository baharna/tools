#!/usr/bin/python3

import struct
import socket

# test IPs to sort
ips = ["192.168.1.1", "11.11.13.10", "192.168.5.6", "200.5.13.200", "10.10.10.1", "127.0.0.1","200.5.13.1", "213.125.123.100", "88.11.88.11"]
# destination list for IPs
sorted_ips = []

# uses socket and struct to convert long format IP back to normal
def convert_to_ip(x):
    reg_ip = socket.inet_ntoa(struct.pack("!L", x))
    return reg_ip

# uses socket and struct to convert ip to long format
def convert_to_long(ip):
    long_ip = struct.unpack("!L", socket.inet_aton(ip))[0]
    return long_ip

def main():
    # calls functio to convert all IPs to longs
    for x in ips:
        sorted_ips.append(convert_to_long(x))
    # sorts list of IPs in long format
    list.sort(sorted_ips)
    # converts long format IPs back to normal format
    for x in sorted_ips:
        sorted_ips[sorted_ips.index(x)] = convert_to_ip(x)
    # prints all IPs to stdout
    for item in sorted_ips:
        print(item)

# calls main function
if __name__ == '__main__':
    main()
