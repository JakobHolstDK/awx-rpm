
import argparse
import glob
import json
import subprocess
import os
import time

PREFIX = 'awx-python36'
PACKAGER = 'Sinan Sert <sis@miracle.dk>'


parser = argparse.ArgumentParser(description='Generate spec files for AWX packages.')
parser.add_argument('build_requires', metavar='build_requires_json', type=str)
parser.add_argument('requires', metavar='requires_json', type=str)
parser.add_argument('pkgs_dir', metavar='packages_directory', type=str)
parser.add_argument('--parse-single', metavar='package_name', type=str)
args = parser.parse_args()

reqs = args.requires
build_reqs = args.build_requires
pkgs_dir = args.pkgs_dir
FNULL = open(os.devnull, 'w')

def generate_spec_for(package_name, reqs_data, build_reqs_data, pkgs_dir):
    pkg_dir = ""
    try:
        pkg_dir = glob.glob(f'{pkgs_dir}/{package_name}/*/')[0]
    except:
        return

    myver = pkg_dir.split('-')[1].split('/')[0]
    pkg_deps = ' '.join([dep['name']+dep['specifier']+dep['version'] for dep in reqs_data[package_name]['dependencies']])

    try:
        probe = build_reqs_data[package_name]['buildrequires']
    except:
        return

    pkg_build_deps = ' '.join([dep['name']+dep['specifier']+dep['version'] for dep in build_reqs_data[package_name]['buildrequires']])
    command = ["python3", "setup.py", "bdist_rpm", "--spec-only",
               "--build-requires", pkg_build_deps, "--packager", PACKAGER, "--dist-dir", "../"]
    if pkg_deps:
        command += ['--requires', pkg_deps]
    subprocess.run(command, cwd=pkg_dir, stdout = FNULL, stderr = FNULL)
    specfile_ = glob.glob(f'{pkgs_dir}/{package_name}/*.spec')[0]
    with open(specfile_, 'r') as specfile:
        temp = specfile.read()
    splitted = temp.split('\n')
    splitted[0] = f'%define name {PREFIX}-{package_name}'
    with open(specfile_, 'w') as specfile:
        specfile.write('\n'.join(splitted))

def prep_pkgsdir(package_name):
    pkg_dir = "%s/%s" % ( pkgs_dir, package_name)
    for file in os.listdir(pkg_dir):
        if file.islower():
            ok = True
        else:
            src = "%s/%s" % (pkg_dir, file)
            dst = "%s/%s" % (pkg_dir, file.lower())
            cmd = "rm %s >/dev/null 2>&1" % (dst)
            os.system(cmd)
            cmd = "mv %s %s >/dev/null 2>&1" % (src,dst)
            os.system(cmd)

def specfile2scl(specfile, pkg_dir):
    command = ["spec2scl", specfile ]
    sclfile = specfile.replace('.spec', '.scl')
    f = open (sclfile, "w")
    subprocess.run(command, stdout = f, stderr = FNULL)
    f.close
    command = ["rpmbuild", "-ba", sclfile ]
    subprocess.run(command, cwd=pkg_dir,  stderr = FNULL)


    return 0



if __name__ == '__main__':
    with open(reqs, 'r') as fp:
        reqs_data = json.load(fp)
    with open(build_reqs, 'r') as fp:
        build_reqs_data = json.load(fp)
    if args.parse_single:
        generate_spec_for(args.parse_single, reqs_data, build_reqs_data, pkgs_dir)
    else:
        for package in reqs_data:
            print("package: %s" % package) 
            prep_pkgsdir(package)
            generate_spec_for(package, reqs_data, build_reqs_data, pkgs_dir)
            specfile = ""
            pkgdir = ""
            validate = False
            try:
                specfile = glob.glob(f'{pkgs_dir}/{package}/*.spec')[0]
                pkgdir = "%s/%s" % (pkgs_dir, package)
                print("specfile : %-30s ; %s" % (package,specfile))
                validate = True
            except:
                print("specfile : %-30s; missing" % (package))

            sf = open(specfile, "r")
            specfiletxt = sf.read()
            for line in specfiletxt.split('\n'):
                if "Require" in line:
                    print(line)
            sf.close

            if validate is True:
                specfile2scl(specfile, pkgdir)


