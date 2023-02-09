#!/bin/bash
# 2023-02-08
# Helper script to see if your system has required packages installed
# Currently, only works on a linux distro (ie Ubuntu), sorry Macs

# set -x

if [ "#$OSTYPE" != "#linux-gnu" ]; then echo "ERR Sorry I don't work on non-linux"; exit 1; fi

packages=('python3.8' 'python3.8-distutils' 'curl' 'libpq-dev' 'python3.8-dev')
echo -n "Looking for packages: "
for pkg in "${packages[@]}"
do
    echo -n "$pkg "
    apt list --installed 2>&1 | grep -e "^${pkg}/" > /dev/null
    e=$?; if [ $e -ne 0 ]; then echo -e "\nERR Missing package $pkg"; exit $e; fi
done
echo -e "\nINF OK, your environment is good to go!"
