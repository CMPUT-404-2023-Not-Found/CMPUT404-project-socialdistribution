#!/bin/bash
# 2023-02-08
# Helper script to see if your system has required packages installed
# Currently, only works on a linux distro (ie Ubuntu), sorry Macs

# set -x

if [ "#$OSTYPE" != "#linux-gnu" ]; then echo "ERR Sorry I don't work on non-linux"; exit 1; fi

# Check for system install packages, libraries, binaries
packages=('python3.8' 'python3-distutils' 'curl' 'libpq-dev' 'python3.8-dev' 'gcc')
echo -ne "Looking for packages:\t"
for pkg in "${packages[@]}"
do
    echo -n "$pkg "
    apt list --installed 2>&1 | grep -e "^${pkg}/" > /dev/null
    e=$?; if [ $e -ne 0 ]; then echo -e "\nERR Missing package $pkg"; exit $e; fi
done
echo ""

# Check for third-party tools 
tools=('heroku' 'node' 'npm' 'npx')
echo -ne "Looking for tools:\t"
for tool in "${tools[@]}"
do
    echo -n "$tool "
    $tool --version > /dev/null 2>&1
    e=$?; if [ $e -ne 0 ]; then echo -e "\nERR Missing tool $tool"; exit $e; fi
done
echo -e "\nINF OK, your environment is good to go!"
