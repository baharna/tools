#!/usr/bin/python3

import argparse
import os
import re
import time
import csv
import textwrap

# Generate a dictionary of hosts and ports contained in the user-specified file

def file_parser(filename):
    f = open(filename, 'r')
    hosts = []
    hostinfo = {}
    for line in f:
        if line[0] != '#':
            # Pull IPs from the user-specified file
            if 'Up' in line:
                word_string = line.split()
                if word_string[1] not in hosts:
                    hosts.append(word_string[1])
            # Pull ports from the user-specified file
            if 'Ports:' in line:
                word_string = line.split()
                host_key = word_string[1]
                ports = []
                pattern = re.compile("([0-9]*)/open/tcp//([a-z]*)///,")
                for item in word_string:
                    if pattern.match(item):
                        port = item.split('/')
                        ports.append(port[0])
                hostinfo.update({host_key:ports})
    f.close()
    # Return the dictionary of hosts and port
    return hostinfo

# Print a detailed report of all hosts and ports in the user-specified file

def detailed(filename):
    hostinfo = file_parser(filename)
    ip_padding = 17
    print("*"*80)
    print("* Detailed View" + " "*64 + "*")
    print("*"*80)
    print("* Hosts" + " "*12 + "* Ports" + " "*53 + "*")
    print("*"*80)
    # Print report wrapping the port list if it is too long
    for key in hostinfo:
        ip_string = "* " + key + " "*(ip_padding - len(key))
        portstring_prepend = "*" + " "*ip_padding
        port_list = textwrap.wrap(', '.join(str(x) for x in hostinfo[key]),width=57)
        for item in port_list:
            print(ip_string + "* " + item + " "*(58-len(item)) + "*")
    print("*"*80)

# Print a report of open ports detected on user-specified hosts

def host(filename, hosts):
    # Generate dictionary list of hosts and ports
    hostinfo = file_parser(filename)
    host_list = hosts.split(',')
    # Validate that the given IPs are valid IPs
    pattern = re.compile("^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
    for host in host_list:
        if not pattern.match(host):
            parser.error("The IP given is not a valid address")
    ip_padding = 15
    print("*"*80)
    label = "* Printing Report on " + str(len(host_list)) + " Hosts"
    print(label + " "*(79 - len(label)) + "*")
    print("*"*80)
    # Print list of hosts and ports, wrapping the port list if it is too long
    for host in host_list:
        for key in hostinfo:
            if host == key:
                ports_open = textwrap.wrap(', '.join(str(x) for x in hostinfo[key]),width=40)
                for item in ports_open:
                        host_string = "* Host IP: "+ key + " "*(ip_padding - len(key)) 
                        port_string = " * Ports Open: " + item 
                        end_padding = " "*(79 - len(host_string) - len(port_string)) + "*"
                        print(host_string + port_string + end_padding)
    print("*"*80)


# Print report on hosts associated with user-identified ports

def port(filename, ports):
    # Generate dictionary list of hosts and ports
    hostinfo = file_parser(filename)
    port_list = ports.split(',')
    # Validate that given ports are integers
    for port in port_list:
        try:
            testport = int(port)
        except ValueError:
            parser.error("Port values must be integers or a comma separated list of integers.")
    # Create dictionary using ports as key
    portinfo = {}
    for ports in port_list:
        portinfo.update({ports:[]})
    print("*"*80)
    ip_padding = 15
    port_padding = 5
    label = "* Printing Report on the Following Ports: " + ','.join(str(port) for port in port_list)
    print(label + " "*(79 - len(label)) + "*")
    print("*"*80)
    # Populate port dictionary with hosts
    for key in hostinfo:
        for port in port_list:
            if port in hostinfo[key]:
                portinfo[port].append(key)
    for port in portinfo:
        hostlist = textwrap.wrap(', '.join(str(x) for x in portinfo[port]),width=55)
        for item in hostlist:
            portstring = "* Ports: " + port + " "*(port_padding - len(port))
            hoststring = " * Hosts: " + item
            end_padding = " "*(79 - len(portstring) - len(hoststring)) + "*"
            print(portstring + hoststring + end_padding)
    print("*"*80)

# Create .csv file in the current directory using timestamp as a filename

def csv_writer(filename):
    hostinfo = file_parser(filename)
    csv_filename = time.strftime("%Y%m%d-%H%M%S")
    csv_filename += ".csv"
    print(csv_filename)
    temp_list = []
    with open(csv_filename, 'w', newline='') as csvfile:
        for host in hostinfo:
            string = ""
            rowwriter = csv.writer(csvfile, delimiter = ',', quotechar = '|', quoting=csv.QUOTE_MINIMAL)
            temp_list.append(host)
            temp_list.extend(hostinfo[host])
            print(temp_list)
            rowwriter.writerow(temp_list)
            temp_list.clear()
    csvfile.close()

# Validate file exists and call appropriate function from user input

def main(args):
    if os.path.isfile(args.filename):
        if args.report == "detailed":
            detailed(args.filename)
        elif args.report == "host":
            host(args.filename, args.hosts)
        elif args.report == "port":
            port(args.filename, args.ports)
        elif args.report == "csv":
            csv_writer(args.filename)
    else:
        print("The specified file does not exist")

# Take arguments and pass to main

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--filename', required=True, help='filename of greppable nmap output')
    parser.add_argument('-r', '--report', help='specifies the type of report to be output', choices=['detailed','host','port','csv'])
    parser.add_argument('--hosts', help='list hosts for host-specific view')
    parser.add_argument('--ports', help='list ports for host-specific view')
    args = parser.parse_args()
    if args.report == "host":
        if args.hosts is None:
            parser.error('One or more hosts must be specified for the host view')
    if args.report == "port":
        if args.ports is None:
            parser.error('One or more ports must be specified for the port view')
    main(args)
