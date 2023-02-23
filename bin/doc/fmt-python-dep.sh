#!/bin/sh
# 2023-02-18
# Take a Python requirement.txt & transform it into a MarkDown table

if [ "#$1" = "#" ]; then echo "Usage $0 </path/to/requirements.txt>"; exit 1; fi
req_txt="$1"

if [ ! -r "$req_txt" ]; then echo "ERR Could not read $req_txt"; exit 1; fi

echo '| Package | Version | Reference |'
echo '| - | - | - |'
# Take 'Django==3.2.18' & make '| Django | 3.2.18 | <https://pypi.org/project/Django> |'
cat "$req_txt" | sed -e 's/^\(.*\)==\(.*\)$/| \1 | \2 | <https:\/\/pypi.org\/project\/\1> |/g'
