#!/usr/bin/python3


ips = ["192.168.1.1", "11.11.13.10", "192.168.5.6", "200.5.13.200", "10.10.10.1", "127.0.0.1","200.5.13.1", "213.125.123.100", "88.11.88.11"]
sorted_ips = []

def even(entry, temp):
    sorted_ips

for item in ips:
    temp = item.split('.')
    if len(sorted_ips) == 0:
        sorted_ips.append('.'.join(temp))
        print("Adding item " + '.'.join(temp))
    else:
        for entry in sorted_ips:
            print("Analyzing " + '.'.join(temp) + " against " + entry)
            if temp[0] < entry.split('.')[0]:
                print("inside the loop")
                idx = sorted_ips.index(entry)
                sorted_ips.insert(sorted_ips.index(entry), '.'.join(temp))
                break
            elif temp[0] == entry.split('.')[0]:
                if temp[1] < entry.split('.')[1]:
                    sorted_ips.insert(sorted_ips.index(entry), '.'.join(temp))
                    break
                elif temp[1] == entry.split('.')[1]:
                    if temp[2] < entry.split('.')[2]:
                        sorted_ips.insert(sorted_ips.index(entry), '.'.join(temp))
                        break
                    elif temp[2] == entry.split('.')[2]:
                        if temp[3] < entry.split('.')[3]:
                            sorted_ips.insert(sorted_ips.index(entry), '.'.join(temp))
                            break
                        elif temp[3] == entry.split('.')[3]:
                            sorted_ips.insert(sorted_ips.index(entry), '.'.join(temp))
                            break
                        else:
                            sorted_ips.insert(sorted_ips.index(entry) + 1, '.'.join(temp))
                            break

                



print(sorted_ips)
