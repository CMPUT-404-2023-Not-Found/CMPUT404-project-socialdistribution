#!/bin/sh
# 2023-02-23
# upd-author.sh
# Update an author

# set -x
if [ "#$APP_URL" = "#" ]; then echo "ERR Could could not find $APP_URL in env, is your env setup?"; exit 1; fi
if [ "#$1" = "#" ]; then echo "Usage $0 [author_uuid]"; exit 1; fi
author_uuid="$1"

if [ ! -r .access_token ]
then
    echo "ERR Could not find a .access_token file, try using ./get-token.sh [username] [password]"
    exit 1
fi

access_token=`cat .access_token`
auth_hdr="Authorization: Bearer $access_token"

upd_author_url="${AUTHOR_API}/$author_uuid/"
rand=`apg -n 1 -m 8 -x 8 -M NC 2`

usr_hst="$APP_URL"
upd_body=`cat <<EOF
{
"displayName": "$rand $usr_hst",
"github": "http://github.com/${rand}_git",
"profileImage": "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=140&q=80"
}
EOF`

rsp=`curl -sX POST \
     -d "$upd_body" \
     -H "Content-Type: application/json" \
     -H "$auth_hdr" \
     "$upd_author_url"`
e=$?; if [ $e -ne 0 ]; then echo -n "ERR Could not POST to $upd_author_url "; echo "$rsp"; exit $e; fi

echo "$rsp" | grep -q "$rand"
e=$?
if [ $e -ne 0 ]
then
    echo "ERR Could not update author $USR_NAME"
    echo "$rsp"
else
    echo "$rsp" | jq 2>/dev/null
    e=$?; if [ $e -ne 0 ]; then echo "$rsp"; exit $e; fi
fi

