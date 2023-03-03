#!/bin/sh
# 2023-02-25
# chg-user.sh
# Symlink some user files to their generic counterpart

# set -x
if [ "#$1" = "#" ]; then echo "Usage $0 <user>"; exit 1; fi
user="$1"
files=".username .password .uuid"
for file in `echo "$files"`
do
    src_file="${user}${file}"
    if [ ! -r "$src_file" ]; then echo "ERR Could not find $src_file"; exit 1; fi
    
    ln -sf $src_file $file
    e=$?; if [ $e -ne 0 ]; then echo "ERR Could not symlink $src_file to $file"; exit $e; fi
done

echo "OK symlinked $user files"

