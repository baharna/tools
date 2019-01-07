#!/usr/bin/python3
# super basic http sniffer

from scapy.all import *

def http_header(packet):
    http_packet = str(packet)
    if http_packet.find('GET'):
        return GET_print(packet)
    if http_packet.find('HTTP/1.1 200 ok'):
        return GET_print(packet)

    
def GET_print(packet1):
    ret = "*"*40 + "GET Packet" + "*"*40
    ret += "\n".join(packet1.sprintf("{Raw:%Raw.load%}\n").split(r"\r\n"))
    ret += "*"*90
    return ret

sniff(iface='eth0', prn=http_header, filter="tcp port 80")
