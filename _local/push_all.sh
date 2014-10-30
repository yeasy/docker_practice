#!/bin/sh
# This script will upload all local images to a registry server ($registry is the default value).
# This script requires the push_images, which can be found at https://github.com/yeasy/docker_practice/blob/master/_local/push_images.sh
# Usage:  push_all
# Author: yeasy@github
# Create: 2014-09-23

for image in `sudo docker images|grep -v "REPOSITORY"|grep -v "<none>"|awk '{print $1":"$2}'`
do
    push_images $image
done

