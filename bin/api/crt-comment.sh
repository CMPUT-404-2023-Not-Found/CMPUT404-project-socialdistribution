#!/bin/bash
# 2023-03-04
# crt-comment.sh
# Create a comment for a post by an author

source .env
# set -x
if [ "#$APP_URL" = "#" ]; then echo "ERR Could could not find $APP_URL in env, is your env setup?"; exit 1; fi
if [ $# -lt 2 ]; then echo "Usage $0 <author_uuid> <post_uuid> [comment]"; exit 1; fi
author_uuid="$1"
post_uuid="$2"
comment="$3"

rand=`echo $RANDOM | md5sum | head -c 8`
comment_text="$rand comment text"
if [ "#$comment" != "#" ]
then
    comment_text="$comment"
fi

crt_body=`cat <<EOF
{
  "comment" : "$comment_text",
  "contentType": "text/plain"
}
EOF`

echo "$crt_body" | jq 2>&1 >/dev/null
e=$?; if [ $e -ne 0 ]; then echo "ERR Invalid POST body"; echo "$crt_body"; exit 1; fi

auth_hdr=$(./get-auth.sh 'bearer' $(cat .username) $(cat .password))
crt_comment_url=`printf "${COMMENT_API}/" $author_uuid $post_uuid`

hdr_dump=`mktemp`
rsp=`curl -sX POST \
     -D "$hdr_dump" \
     -d "$crt_body" \
     -H "Content-Type: application/json" \
     -H "$auth_hdr" \
     "$crt_comment_url"`
e=$?
if [ $e -ne 0 ]
then
    cat "$hdr_dump" >&2
    echo "ERR Failed POST request" >&2
    echo "$rsp"
else
    cat "$hdr_dump" >&2
    echo "$rsp" | jq 2>/dev/null
    e=$?; if [ $e -ne 0 ]; then echo "$rsp"; exit $e; fi
    comment_data=`echo "$rsp" | jq -c 2>/dev/null`
    echo "`date -Iseconds` $comment_data" >> .comment.log
fi
