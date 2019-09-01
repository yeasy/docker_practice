#!/bin/sh

START=`date "+%F %T"`

if [ $1 = "sh" ];then sh ; exit 0; fi

rm -rf node_modules _book

srcDir=$PWD

cp -a . /srv/gitbook

cd /srv/gitbook

main(){
  if [ "$1" = build ];then
    gitbook build && cp -a _book $srcDir && echo $START && date "+%F %T" && exit 0
  else
    exec gitbook serve
  fi
}

main $1 $2 $3
