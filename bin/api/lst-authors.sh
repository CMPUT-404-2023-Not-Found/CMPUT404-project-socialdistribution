#!/bin/sh
# 2023-02-23
# lst-author.sh
# List authors

# set -x
if [ "#$APP_URL" = "#" ]; then echo "ERR Could could not find $APP_URL in env, is your env setup?"; exit 1; fi

LST_AUTHOR_URL="${AUTHOR_API}/"

rsp=`curl -s "$LST_AUTHOR_URL"`
e=$?; if [ $e -ne 0 ]; then echo -n "ERR Could not GET to $LST_AUTHOR_URL "; echo "$rsp"; exit $e; fi

echo "$rsp" | jq 2>/dev/null
e=$?; if [ $e -ne 0 ]; then echo "$rsp"; exit $e; fi

