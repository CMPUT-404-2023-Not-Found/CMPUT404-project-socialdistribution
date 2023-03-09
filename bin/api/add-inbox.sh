#!/bin/sh
# 2023-03-04
# add-inbox.sh
# Add an object to a specific author's inbox

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

add_inbox_url="${AUTHOR_API}/$author_uuid/inbox/"

cnt_body=`cat <<EOF
{
  "@context": "https://www.w3.org/ns/activitystreams",
  "summary": "Shared post",
  "type": "post",
  "author": "http://localhost:8000/api/authors/664925be-f3ce-42b0-9d34-1659d078f840/",
  "object": "http://localhost:8000/api/authors/664925be-f3ce-42b0-9d34-1659d078f840/posts/185389cc-89f2-4714-abdd-6cccbbc24d0e/"
}
EOF`

echo "$cnt_body" | jq 2>&1 >/dev/null
e=$?; if [ $e -ne 0 ]; then echo "ERR Invalid POST body"; exit 1; fi

rsp=`curl -sX POST \
	  -d "$cnt_body" \
	  -H "Content-Type: application/json" \
	  -H "$auth_hdr" \
	  "$add_inbox_url"`
e=$?; if [ $e -ne 0 ]; then echo -n "ERR Could not GET to $add_inbox_url "; echo "$rsp"; exit $e; fi

echo "$rsp" | grep -q "www.w3.org/ns/activitystreams"
e=$?
if [ $e -ne 0 ]
then
    echo "ERR Could not add author $author_uuid's inbox"
    echo "$rsp"
else
    echo "$rsp" | jq 2>/dev/null
    e=$?; if [ $e -ne 0 ]; then echo "$rsp"; exit $e; fi
fi

