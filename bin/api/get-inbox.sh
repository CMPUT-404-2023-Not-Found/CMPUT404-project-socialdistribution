#!/bin/sh
# 2023-03-04
# get-inbox.sh
# Get a specific author's inbox

# set -x
usage () {
    echo "Usage $0 [author_uuid] <page_num> <page_size>" >&2
}

if [ "#$APP_URL" = "#" ]; then echo "ERR Could could not find $APP_URL in env, is your env setup?"; exit 1; fi
if [ "#$1" = "#" ]; then echo "Usage $0 [author_uuid]"; exit 1; fi
author_uuid="$1"

if [ $# -le 1 ]
then
    usage
else
    page_query="?page=${2}"
    if [ "#$3" != "#" ]
    then
        page_query="${page_query}&size=${3}"
    fi
fi

if [ ! -r .access_token ]
then
    echo "ERR Could not find a .access_token file, try using ./get-token.sh [username] [password]"
    exit 1
fi

access_token=`cat .access_token`
auth_hdr="Authorization: Bearer $access_token"

get_inbox_url="${AUTHOR_API}/$author_uuid/inbox/${page_query}"

rsp=`curl -s -H "$auth_hdr" "$get_inbox_url"`
e=$?; if [ $e -ne 0 ]; then echo -n "ERR Could not GET to $get_inbox_url "; echo "$rsp"; exit $e; fi

echo "$rsp" | grep -q "items"
e=$?
if [ $e -ne 0 ]
then
    echo "ERR Could not get author $author_uuid's inbox"
    echo "$rsp"
else
    echo "$rsp" | jq 2>/dev/null
    e=$?; if [ $e -ne 0 ]; then echo "$rsp"; exit $e; fi
fi
