#!/bin/sh
# 2023-03-04
# add-inbox.sh
# Add an object to a specific author's inbox

# set -x
if [ "#$APP_URL" = "#" ]; then echo "ERR Could could not find $APP_URL in env, is your env setup?"; exit 1; fi
if [ $# -lt 4 ]
then
    echo "Usage $0 <author_uuid> <object_author_node_id> <object_type> <object_url> [object_summary]"
    echo "Example:"
    echo " $0 664925be-f3ce-42b0-9d34-1659d078f840 http://localhost:8000/api/authors/398113ca-ce82-420a-b1e8-e8de260d3a64 post http://localhost:8000/api/authors/398113ca-ce82-420a-b1e8-e8de260d3a64/posts/a0dfc41c-4d32-47d1-a567-aed24ae4736e 'This is a shared post'"
    exit 1
fi
author_uuid="$1"
object_author_node_id="$2"
object_type="$3"
object_url="$4"
object_summary="Shared $object_type"
if [ "#$5" != "#" ]
then
    object_summary="$5"
fi

auth_hdr=$(./get-auth.sh 'bearer' $(cat .username) $(cat .password))
add_inbox_url="${AUTHOR_API}/$author_uuid/inbox/"

cnt_body=`cat <<EOF
{
  "@context": "https://www.w3.org/ns/activitystreams",
  "summary": "$object_summary",
  "type": "$object_type",
  "author": { "url": "$object_author_node_id" },
  "object": "$object_url"
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

