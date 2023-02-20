#!/bin/sh
# 2023-02-17
# get-post.sh
# Get a specific post for an author

# set -x
if [ "#$APP_URL" = "#" ]; then echo "ERR Could could not find $APP_URL in env, is your env setup?"; exit 1; fi
if [ "#$1" = "#" -o "#$2" = "#" ]; then echo "Usage $0 [author_uuid] [post_uuid]"; exit 1; fi
author_uuid="$1"
post_uuid="$2"

get_post_url=`printf "${POST_API}/$post_uuid/" $author_uuid`

rsp=`curl -s "$get_post_url"`
e=$?; if [ $e -ne 0 ]; then echo -n "ERR Could not GET to $get_post_url "; echo "$rsp"; exit $e; fi

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

