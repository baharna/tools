#!/usr/bin/python3
# Simple json fuzzer looks for SQLI in json keys
# Tested with Csharpvulnjson https://www.vulnhub.com/entry/csharp-vulnjson,134/

import os
import argparse
import json
import requests

def test(url, enc_json):
    # cycles through json keys
    for key in enc_json.keys():
        # saves json key to revert value after testing
        orig = enc_json[key]
        # tests if value is an integer, if it is it converts it to string for testing
        if isinstance(enc_json[key], int):
            enc_json[key] = str(enc_json[key])
        # appends test string
        enc_json[key] += "'"
        # sends request
        r = requests.post(url, data=json.dumps(enc_json))
        # prints status code
        print("Status code received: " + str(r.status_code))
        # checks for error message
        if "syntax error" in r.text or "unterminated" in r.text:
            print("Possible SQLi in " + key)
        else:
            print("Vulnerability not found in " + key)
        # reverts value
        enc_json[key] = orig

def main(args):
    # formats json and passes url and josn to test method
    file = open(args.filename, "r")
    enc_json = json.loads(file.readlines()[len(file.readlines()) - 1])
    test(args.url, enc_json)
# reads arguments from the command line
# requires -u url argument and a filename
# file should contain a captured requested (from Burp or other proxy) that contains json data)
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', required=True, help='url to connect to')
    parser.add_argument('-f', '--filename', required=True, help='file containing request data to extract json from')
    args = parser.parse_args()
    urltest = False
    if "http://" in args.url or "https://" in args.url:
        urltest = True
    if urltest == False:
        parser.error("URL must include http:// or https://")
    if not os.path.isfile(args.filename):
        parser.error("Filename can't be found")
    main(args)
