#!/bin/sh
# 2023-03-17
# load-data.sh
# load data from the fixtures
# set -x
source .env

if [ "#$FIXTURE_FILES" = "#" ]; then echo "ERR could not find fixture files in your env"; exit 1; fi;
cd ../../

pwd
cd api/
source venv/bin/activate

for FILE in $FIXTURE_FILES
do
	python manage.py loaddata $FILE
done