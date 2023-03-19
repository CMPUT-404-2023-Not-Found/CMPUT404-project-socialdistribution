#!/bin/sh
# 2023-02-23
# lst-author.sh
# List authors

# set -x
usage () {
    echo "Usage $0 [page_num] [page_size]" >&2
}
if [ "#$APP_URL" = "#" ]; then echo "ERR Could could not find $APP_URL in env, is your env setup?"; exit 1; fi
if [ $# -le 0 ]
then
    usage
else
    page_query="?page=${1}"
    if [ "#$2" != "#" ]
    then
        page_query="${page_query}&size=${2}"
    fi
fi

auth_hdr=$(./get-auth.sh 'bearer' $(cat .username) $(cat .password))
LST_AUTHOR_URL="${AUTHOR_API}/${page_query}"

rsp=`curl -s -H "$auth_hdr" "$LST_AUTHOR_URL"`
e=$?; if [ $e -ne 0 ]; then echo -n "ERR Could not GET to $LST_AUTHOR_URL "; echo "$rsp"; exit $e; fi

echo "$rsp" | jq 2>/dev/null
e=$?; if [ $e -ne 0 ]; then echo "$rsp"; exit $e; fi

