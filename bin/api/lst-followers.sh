#!/bin/sh
# 2023-03-23
# lst-follower.sh
# List followers of author_uuid

# set -x
if [ "#$APP_URL" = "#" ]; then echo "ERR Could could not find $APP_URL in env, is your env setup?"; exit 1; fi
if [ $# -ne 1 ]; then echo "Usage $0 <author_uuid>"; exit 1; fi
author_uuid="$1"

lst_follower_url=`printf "${FOLLOWER_API}/" "$author_uuid"`

auth_hdr=$(./get-auth.sh 'bearer' $(cat .username) $(cat .password))
hdr_dump=`mktemp`
rsp=`curl -s \
     -D "$hdr_dump" \
     -H "$auth_hdr" \
     "$lst_follower_url"`
e=$?
if [ $e -ne 0 ]
then
    echo "ERR Could not PUT to $lst_follower_url"
    cat "$hdr_dump"; rm "$hdr_dump"
    echo "$rsp"
    exit $e
else
    cat "$hdr_dump" >&2; rm "$hdr_dump"
    echo "$rsp"
fi

