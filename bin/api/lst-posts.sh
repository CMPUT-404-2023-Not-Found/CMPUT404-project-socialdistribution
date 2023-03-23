#!/bin/sh
# 2023-02-17
# lst-posts.sh
# Get a list of posts for an author

# set -x
usage () {
    echo "Usage $0 <author_uuid|all> [page_num] [page_size]" >&2
    echo "author_uuid: Either specify a specific author_uuid or use all to retrieve all PUBLIC posts on system"
}
if [ "#$APP_URL" = "#" ]; then echo "ERR Could could not find $APP_URL in env, is your env setup?"; exit 1; fi
if [ "#$1" = "#" ]; then usage; exit 1; fi
author_uuid="$1"
if [ $# -le 1 ]
then
    usage
else
    page_query="?page=${2}"
    if [ "#$3" != "#" ]
    then
	page_query="${page_query}&size=${3}"
    fi
fi

auth_hdr=$(./get-auth.sh 'bearer' $(cat .username) $(cat .password))

if [ "#$author_uuid" = "#all" ]
then
    list_post_url="${ALL_POST_API}/${page_query}"
else
    list_post_url=`printf "${POST_API}/${page_query}" $author_uuid`
fi

rsp=`curl -s -H "$auth_hdr" "$list_post_url"`
e=$?; if [ $e -ne 0 ]; then echo -n "ERR Could not GET to $list_post_url"; echo "$rsp"; exit $e; fi

echo "$rsp" | grep -q "$rand"
e=$?
if [ $e -ne 0 ]
then
    echo "ERR Failed GET request"
    echo "$rsp"
else
    echo "$rsp" | jq 2>/dev/null
    e=$?; if [ $e -ne 0 ]; then echo "$rsp"; exit $e; fi
fi

