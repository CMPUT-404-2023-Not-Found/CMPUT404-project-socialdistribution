#!/bin/sh
curl -s http://localhost:8000/api/authors/12fae447-fb43-4cbc-84f9-8965aab66926/followers/ | jq

