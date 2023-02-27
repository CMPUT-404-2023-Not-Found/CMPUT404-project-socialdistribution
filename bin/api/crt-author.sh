#!/bin/sh
# 2023-02-014
# post-author.sh
# Create an author

# set -x
if [ "#$APP_URL" = "#" ]; then echo "ERR Could could not find $APP_URL in env, is your env setup?"; exit 1; fi

CRT_AUTHOR_URL="${AUTHOR_API}/"
RAND=`apg -n 1 -m 8 -x 8 -M NC 2`

USR_NAME="${MONIKER}$RAND"
USR_PWD="P*ssw0rd!"
USR_HST="$APP_URL"
CRT_BODY=`cat <<EOF
{
"username": "$USR_NAME",
"password": "$USR_PWD",
"displayName": "$USR_NAME $USR_HST",
"github": "http://github.com/${USR_NAME}_git",
"profileImage": "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=140&q=80"
}
EOF`

rsp=`curl -s \
     -d "$CRT_BODY" \
     -H "Content-Type: application/json" \
     "$CRT_AUTHOR_URL"`
e=$?; if [ $e -ne 0 ]; then echo -n "ERR Could not POST to $CRT_AUTHOR_URL "; echo "$rsp"; exit $e; fi

echo "$rsp" | grep -q "$RAND"
e=$?
if [ $e -ne 0 ]
then
    echo "ERR Could not create author $USR_NAME"
    echo "$rsp"
else
    echo "$rsp" | jq 2>/dev/null
    e=$?; if [ $e -ne 0 ]; then echo "$rsp"; exit $e; fi
    user_data=`echo "$rsp" | jq -c 2>/dev/null`
    echo "`date -Is` $user_data" >> .author.log
fi

