#!/bin/sh
# 2023-02-17
# lst-posts.sh
# Get a list of posts for an author

# set -x
if [ "#$APP_URL" = "#" ]; then echo "ERR Could could not find $APP_URL in env, is your env setup?"; exit 1; fi
if [ "#$1" = "#" ]; then echo "Usage $0 [author_uuid]"; exit 1; fi
author_uuid="$1"

list_post_url=`printf "${POST_API}/" $author_uuid`

rsp=`curl -s "$list_post_url"`
e=$?; if [ $e -ne 0 ]; then echo -n "ERR Could not GET to $list_post_url"; echo "$rsp"; exit $e; fi

echo "$rsp" | grep -q "$rand"
e=$?
if [ $e -ne 0 ]
then
    echo "ERR Failed GET request"
    echo "$rsp"
else
    echo "$rsp" | jq 2>/dev/null
    e=$?; if [ $e -ne 0 ]; then echo "$rsp"; exit $e; fi
fi

