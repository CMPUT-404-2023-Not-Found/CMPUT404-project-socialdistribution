#!/bin/sh
# 2023-02-014
# post-author.sh
# Create an author

# set -x
if [ -r "../.env" ]; then echo "ERR Could not find ../.env"; exit 1; fi

CRT_AUTHOR_URL="${APP_URL}/${AUTHOR_API}"
RAND=`apg -n 1 -m 6 -x 6 -M NC 2`

USR_NAME="${MONIKER}-$RAND"
USR_PWD="$RAND"
USR_HST="$APP_URL"
CRT_BODY=`cat <<EOF
{
"username": "$USR_NAME",
"password": "$USR_PWD",
"host": "$USR_HST"
}
EOF`

rsp=`curl -sX POST \
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
fi

