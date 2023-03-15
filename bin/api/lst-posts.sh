#!/bin/sh
# 2023-02-17
# lst-posts.sh
# Get a list of posts for an author

# set -x
usage () {
    echo "Usage $0 [author_uuid] <page_num> <page_size>" >&2
}
if [ "#$APP_URL" = "#" ]; then echo "ERR Could could not find $APP_URL in env, is your env setup?"; exit 1; fi
if [ "#$1" = "#" ]; then usage; exit 1; fi
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

list_post_url=`printf "${POST_API}/${page_query}" $author_uuid`

rsp=`curl -s -H "$auth_hdr" "$list_post_url"`
e=$?; if [ $e -ne 0 ]; then echo -n "ERR Could not GET to $list_post_url"; echo "$rsp"; exit $e; fi

echo "$rsp" | grep -q "$rand"
e=$?
if [ $e -ne 0 ]
then
    echo "ERR Failed GET request"
    echo "$rsp"
else
    echo "$rsp" | jq 2>/dev/null
    e=$?; if [ $e -ne 0 ]; then echo "ERR response is not json"; echo "$rsp"; exit $e; fi
fi

