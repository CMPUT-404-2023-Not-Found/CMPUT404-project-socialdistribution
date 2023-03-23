#!/bin/sh
# 2023-03-23
# put-follower.sh
# Put a follower node_id as a new follower of author_uuid

# set -x
if [ "#$APP_URL" = "#" ]; then echo "ERR Could could not find $APP_URL in env, is your env setup?"; exit 1; fi
if [ $# -ne 2 ]; then echo "Usage $0 <author_uuid> <follower_node_id>"; exit 1; fi
author_uuid="$1"
follower_node_id="$2"

follower_node_id_enc=`echo -n "$follower_node_id" | jq -sRr @uri`
put_follower_url=`printf "${FOLLOWER_API}" $author_uuid`
put_follower_url="${put_follower_url}/${follower_node_id_enc}"

auth_hdr=$(./get-auth.sh 'bearer' $(cat .username) $(cat .password))
hdr_dump=`mktemp`
rsp=`curl -sX PUT \
     -D "$hdr_dump" \
     -H "$auth_hdr" \
     "$put_follower_url"`
e=$?
if [ $e -ne 0 ]
then
    echo "ERR Could not PUT to $put_follower_url"
    cat "$hdr_dump"; rm "$hdr_dump"
    echo "$rsp"
    exit $e
else
    cat "$hdr_dump" >&2; rm "$hdr_dump"
    echo "$rsp"
fi

