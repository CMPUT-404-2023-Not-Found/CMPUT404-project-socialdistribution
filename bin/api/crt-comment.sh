#!/bin/sh
# 2023-02-17
# get-post.sh
# Get a specific post for an author

# set -x
if [ "#$APP_URL" = "#" ]; then echo "ERR Could could not find $APP_URL in env, is your env setup?"; exit 1; fi
if [ "#$1" = "#" -o "#$2" = "#"]; then echo "Usage $0 [author_uuid] [post_uuid]"; exit 1; fi
author_uuid="$1"
post_uuid="$2"

if [ ! -r .access_token ]
then
    echo "ERR Could not find a .access_token file, try using ./get-token.sh [username] [password]"
    exit 1
fi

access_token=`cat .access_token`
auth_hdr="Authorization: Bearer $access_token"

crt_comment_url=`printf "${COMMENT_API}/" $author_uuid $post_uuid`
rand=`apg -n 1 -m 8 -x 8 -M NC 2`