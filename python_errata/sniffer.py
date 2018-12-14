#!/usr/bin/python
#needs a lot of work
#need to decode payload section of the data

import struct
import binascii
import socket

def main():
    count = 0
    while count < 20:
        count += 1
        rawSocket = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(0x0800))
        packet = rawSocket.recvfrom(2048)
        print "Packet: ", count
        ethHead = packet[0][0:14]
        print ethHead
        ethHead = struct.unpack("!6s6s2s", ethHead)
        print "\tSource MAC: ", binascii.hexlify(ethHead[0])
        print "\tDestination MAC: ", binascii.hexlify(ethHead[1])
        ipHead = packet[0][14:34]
        ipHead = struct.unpack("!12s4s4s", ipHead)
        print "\tSource IP: ", socket.inet_ntoa(ipHead[1])
        print "\tDestination IP: ", socket.inet_ntoa(ipHead[2])
        tcpHead = packet[0][34:54]
        tcpHead = struct.unpack("!HH16s", tcpHead)
        print "\tSource Port: ", tcpHead[0]
        print "\tDestination Port: ", tcpHead[1]
        tcpData = packet[0][54:len(packet[0])]
        print "\tTCP Data: ", tcpData

if __name__ == '__main__':
    main()
