#!/bin/sh
# 2023-02-23
# lst-author.sh
# List authors

# set -x
if [ "#$APP_URL" = "#" ]; then echo "ERR Could could not find $APP_URL in env, is your env setup?"; exit 1; fi
if [ ! -r .access_token ]
then
    echo "ERR Could not find a .access_token file, try using ./get-token.sh [admin] [password]"
    exit 1
fi

access_token=`cat .access_token`
auth_hdr="Authorization: Bearer $access_token"
LST_AUTHOR_URL="${AUTHOR_API}/"

rsp=`curl -s -H "$auth_hdr" "$LST_AUTHOR_URL"`
e=$?; if [ $e -ne 0 ]; then echo -n "ERR Could not GET to $LST_AUTHOR_URL "; echo "$rsp"; exit $e; fi

echo "$rsp" | jq 2>/dev/null
e=$?; if [ $e -ne 0 ]; then echo "$rsp"; exit $e; fi

