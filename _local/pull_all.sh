#!/bin/sh

# This script will update all local images
# See: https://github.com/yeasy/docker_practice/blob/master/_local/pull_all.sh
# Usage:  pull_all
# Author: yeasy@github
# Create: 2014-09-23

for image in `sudo docker images|grep -v "REPOSITORY"|grep -v "<none>"|awk '{print $1":"$2}'`
do
    sudo docker pull $image
done

