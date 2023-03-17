#!/bin/sh
# 2023-03-17
# basic-curl.sh
# Do curl but with Basic Auth

node_usr=`cat .node-username`
node_pwd=`cat .node-password`
curl -u "${node_usr}:${node_pwd}" "$@"
