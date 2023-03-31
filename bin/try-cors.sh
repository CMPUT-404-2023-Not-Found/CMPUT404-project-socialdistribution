#!/bin/sh

if [ $# -ne 2 ]; then echo "Usage $0 <target_url> <requester_origin>"; exit 1; fi
req_uri="$1"
req_ogn="$2"
req_mtd="GET"

echo "INF Trying $req_uri"
hdr_dump=`mktemp`
rsp=`curl \
    -sv -X OPTIONS -o /dev/null \
    -D "$hdr_dump" \
    -H "Origin: $req_ogn" \
    -H "Access-Control-Request-Method: $req_mtd" \
    "$req_uri" 2>&1`
echo "$rsp" | grep -i '< Access-Control' >/dev/null 2>&1
e=$?
if [ $e -ne 0 ]
then
    cat "$hdr_dump"
    echo "ERR CORS failure. Missing Access-Control-* headers for $req_ogn from $req_uir";
    exit $e
else
    cat "$hdr_dump" | grep -i 'Access-Control'
    echo "OK CORS for $req_uri allows $req_ogn"
fi
