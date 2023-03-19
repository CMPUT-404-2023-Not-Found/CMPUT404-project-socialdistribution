#!/bin/sh
# 2023-03-18
# send-node.sh
# Do a POST node-to-node communication

# set -x
if [ "#$APP_URL" = "#" ]; then echo "ERR Could could not find $APP_URL in env, is your env setup?"; exit 1; fi
if [ $# -lt 3 ]; then echo "Usage $0 <authors_inbox> <foreign_node_url> <object_type> [summary]"; exit 1; fi
authors_inbox="$1"
foreign_node_url="$2"
object_type="$3"

summary="I sent you a $object_type"
if [ "#$4" != "#" ]; then summary="$4"; fi

auth_hdr=$(./get-auth.sh 'bearer' $(cat .username) $(cat .password))

query_param="url=$(echo -n "$authors_inbox" | jq -sRr '@uri')"
send_node_url="${NODE_API}/?${query_param}"
cnt_body=`cat <<EOF
{
  "summary": "$summary",
  "object": "$foreign_node_url",
  "type": "$object_type"
}
EOF`

echo "$cnt_body" | jq 2>&1 >/dev/null
e=$?; if [ $e -ne 0 ]; then echo "ERR Invalid POST body"; exit 1; fi

hdr_dump=`mktemp`
rsp=`curl -sX POST \
     -D "$hdr_dump" \
     -d "$cnt_body" \
     -H "Content-Type: application/json" \
     -H "$auth_hdr" \
     "$send_node_url"`
e=$?
if [ $e -ne 0 ]
then
    echo "ERR Could not POST to $send_node_url"
    cat "$hdr_dump"; rm "$hdr_dump"
    echo "$rsp"
    exit $e
else
    cat "$hdr_dump" >&2; rm "$hdr_dump"
    echo "$rsp"
fi
