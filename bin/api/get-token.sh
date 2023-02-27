#!/bin/sh
# 2023-02-23
# get-token.sh
# Get a JWT access & refresh token

# set -x
if [ "#$APP_URL" = "#" ]; then echo "ERR Could could not find $APP_URL in env, is your env setup?"; exit 1; fi
token_url="$TOKEN_API/"

if [ "#$1" = "#" -o "#$2" = "#" ]
then
    echo "Usage $0 [username] [password]"
    echo "Using defaults in .username .password"
    username=`cat .username`
    password=`cat .password`
else
    username="$1"
    password="$2"
fi

cnt_body=`cat <<EOF
{
"username": "$username",
"password": "$password"
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
	echo "ERR Response does not contain access & refresh token"
	echo "$rsp"
	exit 1
    fi
fi
echo "OK Got a token for $username ... saved to .access_token & .refresh_token"
echo "$rsp" | jq -r .access > .access_token
echo "$rsp" | jq -r .refresh > .refresh_token
