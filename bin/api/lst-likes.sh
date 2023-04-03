#!/bin/sh
# 2023-03-18
# lst-like.sh
# Get a list of likes for a posts or comment

# set -x
usage () {
    echo "Usage $0 <author_uuid> <post_uuid> [comment_uuid] [page_num] [page_size]" >&2
}
if [ "#$APP_URL" = "#" ]; then echo "ERR Could could not find $APP_URL in env, is your env setup?"; exit 1; fi
if [ "#$1" = "#" ]; then usage; exit 1; fi
author_uuid="$1"
post_uuid="$2"
comment_uuid="$3"
if [ $# -le 3 ]
then
    usage
fi

page_num=1
page_size=1

if [ "#$comment_uuid" != "#" ]
then
    if [ "#$4" != "#" ]; then page_num="$4"; fi
    if [ "#$5" != "#" ]; then page_size="$5"; fi
    page_query="?page=${page_num}&size=${page_size}"
    list_like_url=`printf "${COMMENT_API}/${comment_uuid}/likes/${page_query}" $author_uuid $post_uuid`
else
    if [ "#$3" != "#" ]; then page_num="$3"; fi
    if [ "#$4" != "#" ]; then page_size="$4"; fi
    page_query="?page=${page_num}&size=${page_size}"
    list_like_url=`printf "${POST_API}/${post_uuid}/likes/${page_query}" $author_uuid`
fi

auth_hdr=$(./get-auth.sh 'bearer' $(cat .username) $(cat .password))
hdr_dump=`mktemp`
rsp=`curl -s -D "$hdr_dump" -H "$auth_hdr" "$list_like_url"`
e=$?; if [ $e -ne 0 ]; then echo -n "ERR Could not GET to $list_like_url"; echo "$rsp"; exit $e; fi

echo "$rsp" | grep -q "items"
e=$?
if [ $e -ne 0 ]
then
    cat "$hdr_dump" >&2
    echo "ERR Failed GET request" >&2
    echo "$rsp"
else
    cat "$hdr_dump" >&2
    echo "$rsp" | jq 2>/dev/null
    e=$?; if [ $e -ne 0 ]; then echo "$rsp"; exit $e; fi
fi

