#nmap_parser.py
./nmap_parser.py -h
usage: nmap_parser.py [-h] -f FILENAME [-r {detailed,host,port,csv}]
                      [--hosts HOSTS] [--ports PORTS]

optional arguments:
  -h, --help            show this help message and exit
  -f FILENAME, --filename FILENAME
                        filename of greppable nmap output
  -r {detailed,host,port,csv}, --report {detailed,host,port,csv}
                        specifies the type of report to be output
  --hosts HOSTS         list hosts for host-specific view
  --ports PORTS         list ports for host-specific view
