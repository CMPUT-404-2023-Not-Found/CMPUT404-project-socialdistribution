#!/bin/sh
# 2023-03-04
# get-inbox.sh
# Get a specific author's inbox

# set -x
usage () {
    echo "Usage $0 <author_uuid>" >&2
}

if [ "#$APP_URL" = "#" ]; then echo "ERR Could could not find $APP_URL in env, is your env setup?"; exit 1; fi
if [ "#$1" = "#" ]; then usage; exit 1; fi
author_uuid="$1"

auth_hdr=$(./get-auth.sh 'bearer' $(cat .username) $(cat .password))
cnt_inbox_url="${AUTHOR_API}/$author_uuid/inbox/?count"

hdr_dump=`mktemp`
rsp=`curl -s -D "$hdr_dump" -H "$auth_hdr" "$cnt_inbox_url"`
e=$?; if [ $e -ne 0 ]; then echo -n "ERR Could not GET to $cnt_inbox_url "; echo "$rsp"; exit $e; fi

echo "$rsp" | grep -q "count"
e=$?
if [ $e -ne 0 ]
then
    cat $hdr_dump >&2
    echo "ERR Could not get author $author_uuid's inbox count" >&2
    echo "$rsp"
else
    echo "$rsp" | jq 2>/dev/null
    e=$?; if [ $e -ne 0 ]; then echo "$rsp"; exit $e; fi
fi

