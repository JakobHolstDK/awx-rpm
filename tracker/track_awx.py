#!/usr/bin/env python 

import requests
import hashlib


SOURCE_URL = 'https://raw.githubusercontent.com/ansible/awx/devel/requirements/requirements.txt'
def md5(reqtext):
    mysum = hashlib.md5(reqtext.encode('utf-8')).hexdigest() 
    return mysum

def getfile(reqfile):
    resp = requests.get(SOURCE_URL)
    return resp.text

if __name__ == '__main__':
    reqfile = getfile(SOURCE_URL)
    md5sum = md5(reqfile)
    print(md5sum)

