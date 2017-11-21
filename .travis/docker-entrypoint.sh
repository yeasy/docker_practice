#!/bin/sh

START=`date "+%F %T"`

if [ $1 = "sh" ];then sh ; exit 0; fi

rm -rf node_modules _book

cp -a . ../gitbook

cd ../gitbook

main(){
  # gitbook build
  # cp -a _book ../gitbook-src
  gitbook serve
  exit 0
}

main $1 $2 $3
