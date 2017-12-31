#!/bin/sh

START=`date "+%F %T"`

if [ $1 = "sh" ];then sh ; exit 0; fi

rm -rf node_modules _book

cp -a . ../gitbook

cd ../gitbook

main(){
  if [ "$1" = build ];then gitbook build; cp -a _book ../gitbook-src; echo $START; date "+%F %T"; exit 0; fi
  exec gitbook serve
  exit 0
}

main $1 $2 $3
