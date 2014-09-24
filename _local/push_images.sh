#!/bin/sh

# This script will upload the local images to a registry server ($registry is the default value).
# Author: yeasy@github
# Created:2014-09-23

#The registry server address where you want push the images into
registry=127.0.0.1:5000

### DO NOT MODIFY THE FOLLOWING PART, UNLESS YOU KNOW WHAT IT MEANS ###
echo_r () {
    [ $# -ne 1 ] && return 0
    echo -e "\033[31m$1\033[0m"
}
echo_g () {
    [ $# -ne 1 ] && return 0
    echo -e "\033[32m$1\033[0m"
}
echo_y () {
    [ $# -ne 1 ] && return 0
    echo -e "\033[33m$1\033[0m"
}
echo_b () {
    [ $# -ne 1 ] && return 0
    echo -e "\033[34m$1\033[0m"
}

usage() {
    sudo docker images
    echo "Usage: $0 registry1:tag1 [registry2:tag2...]"
}

[ $# -lt 1 ] && usage && exit

echo_b "The registry server is $registry"


for image in "$@"
do
	echo_b "Uploading $image..."
	sudo docker tag $image $registry/$image
	sudo docker push $registry/$image
	sudo docker rmi $registry/$image
	echo_g "Done"
done
