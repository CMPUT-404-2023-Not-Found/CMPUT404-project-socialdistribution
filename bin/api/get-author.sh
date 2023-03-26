#!/bin/sh
# 2023-02-23
# get-author.sh
# Get a specific author

# set -x
if [ "#$APP_URL" = "#" ]; then echo "ERR Could could not find $APP_URL in env, is your env setup?"; exit 1; fi
if [ "#$1" = "#" ]; then echo "Usage $0 [author_uuid]"; exit 1; fi
author_uuid="$1"
auth_hdr=$(./get-auth.sh 'bearer' $(cat .username) $(cat .password))

get_author_url="${AUTHOR_API}/$author_uuid/"

hdr_dump=`mktemp`
rsp=`curl -s -D "$hdr_dump" -H "$auth_hdr" "$get_author_url"`
e=$?; if [ $e -ne 0 ]; then echo -n "ERR Could not GET to $get_author_url "; echo "$rsp"; exit $e; fi

echo "$rsp" | grep -q "$author_uuid"
e=$?
if [ $e -ne 0 ]
then
    cat "$hdr_dump" >&2
    echo "ERR Could not get author" >&2
    echo "$rsp"
    exit $e
else
    cat "$hdr_dump" >&2
    echo "$rsp" | jq 2>/dev/null
    e=$?; if [ $e -ne 0 ]; then echo "$rsp"; exit $e; fi
fi

