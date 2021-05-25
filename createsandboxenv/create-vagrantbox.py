#!/usr/bin/env python

import argparse
import logging
import requests



def parse_args():
   parser = argparse.ArgumentParser(description='Create a vagrantbox from url')
   parser.add_argument('--iso', type=str,
                    help='URL with the ISO')
   parser.add_argument('--kickstart', type=str,
                    help='The kickstartfile')
   args = parser.parse_args()
   return args



def download_iso(ISO):
    resp = requests.get(ISO)
    isofile = resp.text
    print(resp)

def main():
    logging.info('Start')
    args = parse_args()
    download_iso(args.iso)

if __name__ == "__main__":
    main()

