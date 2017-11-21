#!/usr/bin/env bash

# cd .travis
# ./update.sh

if [ ! -f Dockerfile ];then exit 1; fi

cp -a ../book.json book.json
