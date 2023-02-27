#!/bin/sh
# 2023-02-23
# refresh-token.sh
# Refresh a JWT access token with a refresh token

# set -x
if [ "#$APP_URL" = "#" ]; then echo "ERR Could could not find $APP_URL in env, is your env setup?"; exit 1; fi
token_url="$TOKEN_API/refresh/"

if [ ! -r ".refresh_token" ]; then echo "ERR Could not find a .refresh_token to use, try using get-token.sh"; exit 1; fi

token=`cat ".refresh_token"`

cnt_body=`cat <<EOF
{
"refresh": "$token"
}
EOF`

rsp=`curl -sX POST \
     -d "$cnt_body" \
     -H "Content-Type: application/json" \
     "$token_url"`
e=$?; if [ $e -ne 0 ]; then echo -n "ERR Could not POST to $token_url "; echo "$rsp"; exit $e; fi

check_rsp=`echo "$rsp" | jq -r .access 2>/dev/null`
e=$?
if [ $e -ne 0 ]
then
    echo "ERR bad response"
    echo "$rsp"
    exit $e
else
    if [ "#$check_rsp" = "#" ] || [ "#$check_rsp" = "#null" ]
    then
	echo "ERR Response does not contain access token"
	echo "$rsp"
	exit 1
    fi
fi
echo "OK Refreshed token ... saved new tokens to .access_token & .refresh_token"
echo "$rsp" | jq -r .access > .access_token
echo "$rsp" | jq -r .refresh > .refresh_token
