#!/bin/bash
# 2023-03-18
# send-node.sh
# Do a POST node-to-node communication

# set -x
if [ "#$APP_URL" = "#" ]; then echo "ERR Could could not find $APP_URL in env, is your env setup?"; exit 1; fi
if [ $# -lt 4 ]; then echo "Usage $0 <summary> <object_type> <object_url> <inbox_url>"; exit 1; fi
summary="$1"
object_type="$2"
object_url="$3"
shift; shift; shift

auth_hdr=$(./get-auth.sh 'bearer' $(cat .username) $(cat .password))

# This code is modified from a forum answer from nisetama, last edited on 2022-10-07, retrieved on 2023-03-18, from stackoverflow.com
# forum answer here:
# https://stackoverflow.com/questions/296536/how-to-urlencode-data-for-curl-command
for inbox_url in "$@"
do
    query_param="${query_param}url=$(echo -n "$inbox_url" | jq -sRr '@uri')&"
done

# This code is modified from a tutorial on cut from @Pushpender007, last updated 2021-06-29, retrieved on 2023-03-19, from geeksforgeeks.org
# tutorial here:
# https://www.geeksforgeeks.org/remove-last-character-from-string-in-linux/
query_param=$(echo "$query_param" | rev | cut -c 2- | rev)

send_node_url="${NODE_API}/?${query_param}"
cnt_body=`cat <<EOF
{
  "summary": "$summary",
  "object": "$object_url",
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
