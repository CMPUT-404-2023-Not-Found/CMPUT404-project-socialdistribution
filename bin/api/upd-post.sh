#!/bin/sh
# 2023-02-17
# upd-post.sh
# Update a post for an author

# set -x
if [ "#$APP_URL" = "#" ]; then echo "ERR Could could not find $APP_URL in env, is your env setup?"; exit 1; fi
if [ "#$1" = "#" -o "#$2" = "#" ]; then echo "Usage $0 [author_uuid] [post_uuid]"; exit 1; fi
author_uuid="$1"
auth_hdr=$(./get-auth.sh 'bearer' $(cat .username) $(cat .password))

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
e=$?; if [ $e -ne 0 ]; then echo "ERR Invalid POST body"; exit 1; fi

hdr_dump=`mktemp`
rsp=`curl -sX POST \
     -D "$hdr_dump" \
     -d "$crt_body" \
     -H "$auth_hdr" \
     -H "Content-Type: application/json" \
     "$upd_post_url"`
e=$?; if [ $e -ne 0 ]; then echo -n "ERR Could not POST to $upd_post_url "; echo "$rsp"; exit $e; fi

echo "$rsp" | grep -q "$rand"
e=$?
if [ $e -ne 0 ]
then
    cat $hdr_dump >&2
    echo "ERR Failed POST request" >&2
    echo "$rsp" >&2
else
    echo "$rsp" | jq 2>/dev/null
    e=$?; if [ $e -ne 0 ]; then echo "$rsp"; exit $e; fi
    post_data=`echo "$rsp" | jq -c 2>/dev/null`
    echo "`date -Is` $post_data" >> .post.log
fi

