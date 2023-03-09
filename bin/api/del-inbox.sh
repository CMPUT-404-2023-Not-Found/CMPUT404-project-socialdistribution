#!/bin/sh
# 2023-03-06
# del-inbox.sh
# Delete a specific author's inbox

# set -x
usage () {
    echo "Usage $0 [author_uuid] <page_num> <page_size>" >&2
}

if [ "#$APP_URL" = "#" ]; then echo "ERR Could could not find $APP_URL in env, is your env setup?"; exit 1; fi
if [ "#$1" = "#" ]; then echo "Usage $0 [author_uuid]"; exit 1; fi
author_uuid="$1"

if [ ! -r .access_token ]
then
    echo "ERR Could not find a .access_token file, try using ./get-token.sh [username] [password]"
    exit 1
fi

hdr_dump=`mktemp`
access_token=`cat .access_token`
auth_hdr="Authorization: Bearer $access_token"

del_inbox_url="${AUTHOR_API}/$author_uuid/inbox/${page_query}"

rsp=`curl -D "$hdr_dump" -sX DELETE -H "$auth_hdr" "$del_inbox_url"`
e=$?; if [ $e -ne 0 ]; then echo -n "ERR Could not DELETE $del_inbox_url "; echo "$rsp"; exit $e; fi
cat "$hdr_dump"; rm "$hdr_dump"


