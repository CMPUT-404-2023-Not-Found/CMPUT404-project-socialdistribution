#!/bin/bash
# 2023-03-18
# send-node.sh
# Do a POST node-to-node communication

# set -x
usage () {
    echo "Usage $0 <summary> <object_type> <object_url> <inbox_url> [more_inbox_urls...]"
    echo "summary: I Liked Your Post"
    echo "object_type: like"
    echo "object_url: http://somesite/api/authors/<owner_of_post_i_liked>/posts/<post_i_liked>/"
    echo "inbox_url: http://somesite/api/authors/<owner_of_post_i_liked>/inbox/"
    echo "more_inbox_urls: space seperated additional inbox urls"
}
if [ "#$APP_URL" = "#" ]; then echo "ERR Could could not find $APP_URL in env, is your env setup?"; exit 1; fi
if [ $# -lt 4 ]; then usage; exit 1; fi
summary="$1"
object_type="$2"
object_url="$3"
shift; shift; shift

auth_hdr=$(./get-auth.sh 'bearer' $(cat .username) $(cat .password))

inbox_urls=''
for inbox_url in "$@"
do
    inbox_urls="${inbox_urls}\"${inbox_url}\","
done
inbox_urls="[$(echo "${inbox_urls}" | rev | cut -c2- | rev)]"


send_node_url="${NODE_API}/"
cnt_body=`cat <<EOF
{
  "summary": "$summary",
  "object": "$object_url",
  "type": "$object_type",
  "inbox_urls": $inbox_urls
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
