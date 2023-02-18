#!/bin/sh
# 2023-02-17
# put-post.sh
# Update/create a post for an author at an id

# set -x
if [ "#$APP_URL" = "#" ]; then echo "ERR Could could not find $APP_URL in env, is your env setup?"; exit 1; fi
if [ "#$1" = "#" -o "#$2" = "#" ]; then echo "Usage $0 [author_uuid] [post_uuid]"; exit 1; fi
author_uuid="$1"
post_uuid="$2"

upd_post_url=`printf "${POST_API}/${post_uuid}/" $author_uuid`
rand=`apg -n 1 -m 8 -x 8 -M NC 2`

crt_body=`cat <<EOF
{
  "unlisted": false,
  "visibility": "PUBLIC",
  "content": "$rand Content",
  "contentType": "text/plain",
  "description": "$rand Desc",
  "title": "$rand Title"
}
EOF`

echo "$crt_body" | jq 2>&1 >/dev/null
e=$?; if [ $e -ne 0 ]; then echo "ERR Invalid PUT body"; exit 1; fi

rsp=`curl -sX PUT \
     -d "$crt_body" \
     -H "Content-Type: application/json" \
     "$upd_post_url"`
e=$?; if [ $e -ne 0 ]; then echo -n "ERR Could not PUT to $upd_post_url "; echo "$rsp"; exit $e; fi

echo "$rsp" | grep -q "$rand"
e=$?
if [ $e -ne 0 ]
then
    echo "ERR Failed PUT request"
    echo "$rsp"
else
    echo "$rsp" | jq 2>/dev/null
    e=$?; if [ $e -ne 0 ]; then echo "$rsp"; exit $e; fi
    post_data=`echo "$rsp" | jq -c 2>/dev/null`
    echo "`date -Is` $post_data" >> .post.log
fi

