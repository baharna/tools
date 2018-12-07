#!/usr/bin/python

import threading
import socket
import ipaddress

class SubnetError(Exception):
    pass

class IPError(Exception):
    pass

def scan(ip):
    scanner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    scanner.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        scanner.connect((str(ip), 9001))
        print "Successful"
    except:
        print "port not open"


def singleIP(ip):
    print "The IP is " + ip
    scan(ip)

def subnetScan(ip):
    print "The subnet is " + ip

def main():
    while True:
        subnet = unicode(raw_input("Enter the subnet in X.X.X.X/X format or a single IP in X.X.X.X format: "))
        check = subnet.split("/")
        try:
            check_ip = check[0].split(".")
            for item in check_ip:
                if 0 > int(item) or int(item) > 254 or len(check_ip) > 4 or len(check_ip) < 4:
                    raise IPError
            if len(check) == 1:
                singleIP(check[0])
                break
            else:
                check1 = check[1]
                print check1
                if int(check1) < 1 or int(check1) > 32:
                    raise SubnetError
                subnetScan(subnet)
        except SubnetError:
            print "boo not a subnet"
        except IPError:
            print "not a valid address"
        break


if __name__ == '__main__':
    main()
