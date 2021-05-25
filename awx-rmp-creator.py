#!/usr/bin/env python
import requests
import logging

logging.debug('This is a debug message')
logging.info('This is an info message')
logging.warning('This is a warning message')
logging.error('This is an error message')
logging.critical('This is a critical message')



SOURCE_URL = 'https://raw.githubusercontent.com/ansible/awx/devel/requirements/requirements.txt'
PACKAGES_DIR = 'packages'
EXTRA_PACKAGES_DIR = 'extrapackages'
DEPENDENT_PACKAGES_DIR = 'dependent_packages'

pypi_session = requests.sessions.Session()

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


def main():
    logging.info('Collect the requirement file')
    fetch_all_from_source()

if __name__ == "__main__":
    main()
