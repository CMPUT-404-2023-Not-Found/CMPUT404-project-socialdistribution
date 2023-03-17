#!/bin/bash
# 2023-03-04
# crt-comment.sh
# Create a comment for a post by an author

source .env
# set -x
if [ "#$APP_URL" = "#" ]; then echo "ERR Could could not find $APP_URL in env, is your env setup?"; exit 1; fi
if [ "#$1" = "#" -o "#$2" = "#" ]; then echo "Usage $0 [author_uuid] [post_uuid]"; exit 1; fi
author_uuid="$1"
auth_hdr=$(./get-auth.sh 'bearer' $(cat .username) $(cat .password))
post_uuid="$2"
crt_comment_url=`printf "${COMMENT_API}/" $author_uuid $post_uuid`

rand=`echo $RANDOM | md5sum | head -c 8`
crt_body=`cat <<EOF
{
  "comment" : "$rand Content",
  "contentType": "text/plain"
}
EOF`

echo "$crt_body" | jq 2>&1 >/dev/null
e=$?; if [ $e -ne 0 ]; then echo "ERR Invalid POST body"; echo "$crt_body"; exit 1; fi

rsp=`curl -sX POST \
     -d "$crt_body" \
     -H "Content-Type: application/json" \
     -H "$auth_hdr" \
     "$crt_comment_url"`
e=$?; if [ $e -ne 0 ]; then echo -n "ERR Could not POST to $crt_comment_url "; echo "$rsp"; exit $e; fi

echo "$crt_comment_url";
echo "$rsp" | grep -q "$rand"
e=$?
if [ $e -ne 0 ]
then
    echo "ERR Failed POST request"
    echo "$rsp"
else
    echo "$rsp" | jq 2>/dev/null
    e=$?; if [ $e -ne 0 ]; then echo "$rsp"; exit $e; fi
    comment_data=`echo "$rsp" | jq -c 2>/dev/null`
    echo "`date -Iseconds` $comment_data" >> .comment.log
fi
