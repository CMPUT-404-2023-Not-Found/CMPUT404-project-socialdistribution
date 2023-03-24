#!/bin/sh
req_ogn="https://social-t30.herokuapp.com"
req_mtd="GET"
req_hdr="X-PINGOTHER"
req_uri="https://sd-7-433-api.herokuapp.com/api/authors/d3bb924f-f37b-4d14-8d8e-f38b09703bab/posts/1629b94f-04cc-459e-880e-44ebe979fb7e/"

echo "Trying $req_uri"
rsp=`curl \
    -sv -X OPTIONS -o /dev/null \
    -H "Origin: $req_ogn" \
    -H "Access-Control-Request-Method: $req_mtd" \
    -H "Access-Control-Request-Headers: $req_hdr" \
    "$req_uri" 2>&1`
#echo "$rsp"
echo "$rsp" | grep -i '< Access-Control'
e=$?
if [ $e -ne 0 ]; then echo "Fail"; echo "$rsp"; exit 1; fi