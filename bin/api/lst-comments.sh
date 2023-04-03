#!/bin/sh
# 2023-03-17
# lst-comments.sh
# Get a list of comments on a post for an author

# set -x
usage () {
    echo "Usage $0 <author_uuid> <post_uuid> [page_num] [page_size]" >&2
}
if [ "#$APP_URL" = "#" ]; then echo "ERR Could could not find $APP_URL in env, is your env setup?"; exit 1; fi
if [ "#$1" = "#" -o "#$2" = "#" ]; then echo "Usage $0 [author_uuid] [post_uuid]"; exit 1; fi
author_uuid="$1"
post_uuid="$2"

if [ $# -le 2 ]
then
    usage
else
    page_query="?page=${3}"
    if [ "#$3" != "#" ]
    then
	page_query="${page_query}&size=${4}"
    fi
fi

auth_hdr=$(./get-auth.sh 'bearer' $(cat .username) $(cat .password))
list_comment_url=`printf "${COMMENT_API}/${page_query}" $author_uuid $post_uuid`

hdr_dump=`mktemp`
rsp=`curl -s -D "$hdr_dump" -H "$auth_hdr" "$list_comment_url"`
e=$?; if [ $e -ne 0 ]; then echo -n "ERR Could not GET to $list_comment_url"; echo "$rsp"; exit $e; fi

echo "$rsp" | grep -q "$rand"
e=$?
if [ $e -ne 0 ]
then
    cat "$hdr_dump" >&2
    echo "ERR Failed GET request"
    echo "$rsp"
else
    cat "$hdr_dump" >&2
    echo "$rsp" | jq 2>/dev/null
    e=$?; if [ $e -ne 0 ]; then echo "$rsp"; exit $e; fi
fi

