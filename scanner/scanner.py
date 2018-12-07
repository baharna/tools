#!/usr/bin/python
#work in progress, uses Seclists nmap top 1000 list

import threading
import socket
import ipaddress

class SubnetError(Exception):
    pass

class IPError(Exception):
    pass

def port_input():
    while True:
        ports = raw_input('Enter the port or multiple ports separated by a comma (Leave blank to use top 1000 ports): ')
        ports = ports.split(',')
        if len(ports) == 1:
            if ports[0] == '':
                portlist = []
                file = open('nmap-top1000-ports.txt', 'r')
                file = file.readlines()
                file = file[0].rstrip()
                for item in file.split(','):
                    if '-' in item:
                        sublist = item.split('-')
                        for subitem in range(int(sublist[0]), (int(sublist[1]) + 1)):
                            portlist.append(subitem)
                    else:
                        portlist.append(item)
                return portlist
            else:
                print ports
                return 'scan port'
        else:
            return 'iterate through ports and return a port list'


def scan(ip, portlist = [5040]):
    scanner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    scanner.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    count = 0
    for item in portlist:
        count += 1
        try:
            scanner.connect((str(ip), int(item)))
            print 'Successful scan of ' + ip + ' on port ' + str(item)
        except:
            #print 'port ' + str(item) + ' not open on host ' + ip
            pass
    print 'Attempted to scan ' + str(count) + ' ports'

def singleIP(ip):
    print 'The IP is ' + ip
    portlist = port_input()
    scan(ip, portlist)

def subnetScan(subnet):
    print 'The subnet is ' + subnet
    threads = []
    for address in ipaddress.ip_network(subnet):
        t = threading.Thread(target=scan, args=(str(address),))
        threads.append(t)
        t.start()
def main():
    while True:
        subnet = unicode(raw_input('Enter the subnet in X.X.X.X/X format or a single IP in X.X.X.X format: '))
        check = subnet.split('/')
        try:
            check_ip = check[0].split('.')
            for item in check_ip:
                if 0 > int(item) or int(item) > 254 or len(check_ip) > 4 or len(check_ip) < 4:
                    raise IPError
            if len(check) == 1:
                singleIP(check[0])
                break
            else:
                check1 = check[1]
                if int(check1) < 1 or int(check1) > 32:
                    raise SubnetError
                subnetScan(subnet)
        except SubnetError:
            print 'boo not a subnet'
        except IPError:
            print 'not a valid address'
        break


if __name__ == '__main__':
    main()
