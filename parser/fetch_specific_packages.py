#!/usr/bin/env python 

import json
import os
import re
import shutil
from collections import deque

import requests
import requirements
from pip._internal.models.target_python import TargetPython
from pip._internal.models.format_control import FormatControl
from pip._internal.index.collector import LinkCollector
from pip._internal.network.session import PipSession
from pip._internal.models.search_scope import SearchScope
from pip._internal.index.package_finder import PackageFinder
from pip._vendor.packaging.specifiers import SpecifierSet







SOURCE_URL = 'https://raw.githubusercontent.com/ansible/awx/devel/requirements/requirements.txt'
PACKAGES_DIR = 'packages'

def download_package(package_name, specifier='', path=PACKAGES_DIR):
    print(f'download_best_package: {package_name}')
    name, version, url = get_best_package(package_name, specifier)
    url_split = url.split('#sha256')[0]
    file_split = url_split.split('/')[-1]
    dest = f'{path}/{name}/{file_split}'

    if not os.path.exists(f'{path}/{name}'):
        os.makedirs(f'{path}/{name}')

    # Only download in not done previously
    if not os.path.isfile(dest):
        print(f'Downloading: {url_split}')
        r = requests.get(url_split, allow_redirects=True)
        open(dest, 'wb').write(r.content)
        shutil.unpack_archive(dest, f'{path}/{package_name}')
        extracted = dest.rstrip('.tar.gz')
        try:    
            os.rename(extracted, extracted.lower())
        except:
            return

def get_best_package(package_name, specifier=''):
    print(f'get_best_package: {package_name}')
    allow_yanked = True
    ignore_requires_python = True
    target_python = TargetPython(py_version_info=(3, 8, 3))
    format_control = FormatControl({':all:'}, {})
    link_collector = LinkCollector(
        session=PipSession(),
        search_scope=SearchScope([], ['https://pypi.org/simple']),
    )
    finder = PackageFinder(
        link_collector=link_collector,
        target_python=target_python,
        allow_yanked=allow_yanked,
        format_control=format_control,
        ignore_requires_python=ignore_requires_python,
    )
    cand = finder.find_best_candidate(package_name, SpecifierSet(specifier))
    return cand.best_candidate.name, cand.best_candidate.version, cand.best_candidate.link.url


def get_package_info(package):
    print(f'get_package_info: {package}')
    url = 'https://pypi.python.org/pypi/' + package + '/json'
    response = pypi_session.get(url, allow_redirects=True)
    data = response.json()
    return data


# fetch requirements.txt
def fetch_all_from_source():
    print("### In fetch_all_from_source ###")
    resp = requests.get(SOURCE_URL)
    pkgs = resp.text
    packages = []
    for pkg in requirements.parse(pkgs):
        packages.append({
            'name': pkg.name,
            'specifier': pkg.specs[0][0] if pkg.specs else '',
            'version': pkg.specs[0][1] if pkg.specs else ''
        })
    return packages


def download_all_packages():
    if not os.path.exists(PACKAGES_DIR):
        os.makedirs(PACKAGES_DIR)

    for pkg in condensed.values():
        print(f'Downloading {pkg["name"]}')
        download_package(pkg['name'], specifier='=='+pkg['definite_version'])


if __name__ == '__main__':
   print("### In fetch_all_from_source ###")
   resp = requests.get(SOURCE_URL)
   pkgs = resp.text
   for pkg in requirements.parse(pkgs):
           name      = pkg.name
           target = "%s%s" % (pkg.specs[0][0], pkg.specs[0][1])
           download_package(name, target)
           pipinstall = "pip install %s%s" % (name, target)
           os.system(pipinstall)
   cmd = "python -m pip freeze >requirements.full.txt"
   os.system(cmd)
   f = open("requirements.full.txt", "r")
   pkgs = f.read()
   for pkg in requirements.parse(pkgs):
           name      = pkg.name.lower()
           target = "%s%s" % (pkg.specs[0][0], pkg.specs[0][1])
           try:
               download_package(name, target)
           except:
               print("Already downloaded")
           pipinstall = "pip install %s%s" % (name, target)




   print("### The end ###")

#   with open('out.json', 'w') as out:
#   	json.dump(fetched_list, out, indent=4)
#   download_all_packages('out.json')

