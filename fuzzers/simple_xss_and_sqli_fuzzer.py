#!/usr/bin/python3
# Simple fuzzer concept based on Grey Hat C# work
# Tested with Badstore vulnerable machine from vulnhub
# https://www.vulnhub.com/entry/badstore-123,41/

import socket
import requests
import argparse
import urllib3

def inject(url, params, append):
    # Disable warning about insecure TLS
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    # Break parameters into key/value pairs for requests
    params = dict(i.split('=') for i in params.split('&'))
    for key in params.keys():
        # Cycle through parameters, append test string, send to url
        orig = params[key]
        params[key] += append
        r = requests.get(url, params, verify=False)
        # Ensure the url responds with 200
        if r.status_code != 200:
            print("Something went wrong")
        # Check for XSS
        elif "<xss>" in r.text:
            print("\t[!!!!] Possible XSS found in parameter " + key)
        # Check for SQLi
        elif "error in your SQL syntax" in r.text:
            print("\t[!!!!] Possible SQLi found in parameter " + key)
        else:
            print("\t[+] Nothing found in parameter " + key)
        # Reset value to original 
        params[key] = orig

def main(args):
    # Break url into the url and parameter
    params = args.url.split('?')[1]
    url = args.url.split('?')[0]
    print("[+] Testing XSS...")
    inject(url, params, "<xss>")
    print("[+] Testing SQLi...")
    inject(url, params, "'")

if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', required=True, help="url with parameters to be tested")
    args = parser.parse_args()
    # Simple test to check for a url and ensure it has parameters to test
    urltest = False
    if "http://" in args.url or "https://" in args.url:
        urltest = True
    if urltest == False:
        parser.error("URL must include http:// or https:// prefix")
    if not args.url.split('?')[1]:
        parser.error("No parameters found to inject")
    main(args)
