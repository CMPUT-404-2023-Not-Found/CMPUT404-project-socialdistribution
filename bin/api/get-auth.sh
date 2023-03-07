#!/bin/sh
# 2023-03-07
# get-auth.sh
# Get the authorization header

usage() {
    echo "Usage $0 <authType> <username> <password>"
    echo "authType: basic, bearer"
}

if [ $# -ne 3 ]; then usage; exit 1; fi
auth_type="$1"
username="$2"
password="$3"

if [ "#$auth_type" = "#bearer" ]
then
    token_file='.access_token'
    ./get-token.sh "$username" "$password" >/dev/null 2>&1
    e=$?; if [ $e -ne 0 ]; then echo "ERR Could not call ./get-token $username $password" >&2; exit $e; fi
    auth_val=`cat $token_file`
    echo "Authorization: Bearer $auth_val"
elif [ "#$auth_type" = "#basic" ]
then
    auth_val=`echo -n "${username}:${password}" | base64`
    e=$?; if [ $e -ne 0 ]; then echo "ERR Could not base64 ${username}:${password}" >&2; exit $e; fi
    echo "Authorization: Basic $auth_val"
fi
