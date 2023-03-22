#!/bin/sh
# 2023-03-18
# get-node.sh
# Do a GET node-to-node communication

# set -x
usage () {
    echo "Usage $0 <object_type> <object_url>"
    echo "object_type: post, like, author, comment"
    echo "object_url: http://somesite/service/authors/<uuid>"
}
if [ "#$APP_URL" = "#" ]; then echo "ERR Could could not find $APP_URL in env, is your env setup?"; exit 1; fi
if [ "#$1" = "#" -o "#$2" = "#" ]; then usage; exit 1; fi
object_type="$1"
foreign_node_url="$2"

auth_hdr=$(./get-auth.sh 'bearer' $(cat .username) $(cat .password))
get_node_url="${NODE_API}/"

hdr_dump=`mktemp`
rsp=`curl -sG \
     -D "$hdr_dump" \
     -H "$auth_hdr" \
     --data-urlencode "type=${object_type}" \
     --data-urlencode "url=${foreign_node_url}" \
     "$get_node_url"`
e=$?
if [ $e -ne 0 ]
then
    echo "ERR Could not GET to $get_node_url"
    cat "$hdr_dump"; rm "$hdr_dump"
    echo "$rsp"
    exit $e
else
    cat "$hdr_dump" >&2; rm "$hdr_dump"
    echo "$rsp"
fi
