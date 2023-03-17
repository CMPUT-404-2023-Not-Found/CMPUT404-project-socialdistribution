#!/bin/sh
# 2023-03-17
# basic-curl.sh
# Do curl but with Basic Auth

node_usr=`cat .node-username`
node_pwd=`cat .node-password`
hdr_dump=`mktemp`

curl -D "$hdr_dump" -u "${node_usr}:${node_pwd}" "$@"
echo ""
echo "Response headers can be found in hdr_dump [$hdr_dump]" >&2
