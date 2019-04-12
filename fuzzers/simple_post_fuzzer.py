#!/usr/bin/python3
# Simple fuzzer that looks for SQLi in parameters taken from a request saved in a file
# Tested using Badtore VM from https://www.vulnhub.com/entry/badstore-123,41/

import requests
import argparse
import urllib3

def test(post_string, url):
    params = post_string.split("&")
    count = 0
    vuln = []
    for item in params:
        orig = item
        params[count] = params[count] +  "'"
        params_send = "&".join(params)
        print("[+] Testing " + url + " with parameter " + params[count])
        r = requests.post(url, data=params_send, verify=False)
        if "error in your SQL syntax" in r.text:
            if params[count].split("=")[0] not in vuln:
                vuln.append(params[count].split("=")[0])
        params[count] = orig
        count += 1
    r = requests.post(url, data=params_send)
    if vuln:
        for item in vuln:
            print("[!!!!] " + item + " parameter seems vulnerable to SQL injection")
    else:
        print("[-] No items seem vulnerable to SQL injection")

def main(args):
    filename = args.filename
    file = open(filename, "r")
    lines = file.readlines()
    post_string = lines[len(file.readlines()) - 1]
    host = ""
    url = ""
    for line in lines:
        if "Host:" in line:
            host = line.split(" ")[1]
        if "POST" in line:
            url = line.split(" ")[1] 
    # checks for https and sets prepend value accordingly
    if args.https:
        prepend = "https://"
    else:
        prepend = "http://"
    # sets the url and sends it with the post sting to the test function
    if host and url:
        url = prepend + host.strip() + url
        test(post_string.strip(), url)
    else:
        print("Request format invalid, check the file")

if __name__ == "__main__":
    # takes in filename and optional https option
    # https doesn't want to work with badstore, even with verify turned off
    # possible I'm just bad, will keep trying later
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", required=True, help="file containing POST request to extract data from")
    parser.add_argument("--https", required=False, action="store_true", help="specify connecting to an https site")
    args = parser.parse_args()
    main(args)
