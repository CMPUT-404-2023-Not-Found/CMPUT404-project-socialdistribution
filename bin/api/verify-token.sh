#!/bin/sh
# 2023-02-23
# verify-token.sh
# Verify a JWT token

# set -x
if [ "#$APP_URL" = "#" ]; then echo "ERR Could could not find $APP_URL in env, is your env setup?"; exit 1; fi
token_url="$TOKEN_API/verify/"
if [ "#$1" = "#" ]; then echo "Usage $0 <token_file>"; exit 1; fi
token_file="$1"
if [ ! -r "$token_file" ]; then echo "ERR Could not find $token_file"; exit 1; fi

token=`cat "$token_file"`

cnt_body=`cat <<EOF
{
"token": "$token"
}
EOF`

rsp=`curl -sX POST \
     -d "$cnt_body" \
     -H "Content-Type: application/json" \
     "$token_url"`
e=$?; if [ $e -ne 0 ]; then echo -n "ERR Could not POST to $token_url "; echo "$rsp"; exit $e; fi

is_valid=`echo "$rsp" | jq -r '.error[]' 2>/dev/null`
if [ "#$is_valid" != "#" ] || [ "#$is_valid" != "#null" ]
then
    echo "ERR $token_file is bad"
    echo "$rsp"
else
    echo "OK $token_file is legit"
fi
