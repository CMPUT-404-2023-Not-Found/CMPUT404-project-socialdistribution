#!/bin/sh
# 2023-03-04
# get-comment.sh
# Get a specific comment for a post

# set -x
if [ "#$APP_URL" = "#" ]; then echo "ERR Could could not find $APP_URL in env, is your env setup?"; exit 1; fi
if [ "#$1" = "#" -o "#$2" = "#" -o "#$3" = "#" ]; then echo "Usage $0 [author_uuid] [post_uuid] [comment_uuid]"; exit 1; fi
author_uuid="$1"
post_uuid="$2"
comment_uuid="$3"

get_comment_url=`printf "${COMMENT_API}/$comment_uuid/" $author_uuid $post_uuid`

rsp=`curl -s "$get_comment_url"`
e=$?; if [ $e -ne 0 ]; then echo -n "ERR Could not GET to $get_comment_url "; echo "$rsp"; exit $e; fi

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

