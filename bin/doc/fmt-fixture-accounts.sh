#!/bin/sh
# 2023-02-18
# Take a JSON fixtures.json file & transform it into a MarkDown table

if [ "#$1" = "#" ]; then echo "Usage $0 </path/to/fixtures.json>"; exit 1; fi
fix_json="$1"

if [ ! -r "$fix_json" ]; then echo "ERR Could not read $fix_json"; exit 1; fi

cat "$fix_json" | jq -rc '.[] | { pk:.pk, username: .fields.username, is_superuser: .fields.is_superuser, is_active: .field.is_active}'
