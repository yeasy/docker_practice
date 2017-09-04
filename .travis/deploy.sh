#!/bin/bash
pwd
git clone -b gh-pages "$REPO" .deploy_git
if [ ! $? = 0 ];then
  #不存在
  echo -e "\033[31mINFO\033[0m  BRANCH <gh-pages> NOT exist"
  mkdir .deploy_git
  cd .deploy_git
  git init
  git remote add origin $REPO
  git checkout -b gh-pages
  cd ..
else
  #存在
  git ls-files | while read file; do touch -d $(git log -1 --format="@%ct" "$file") "$file"; done
  echo -e "\033[32mINFO\033[0m  BRANCH exist"
  rm -rf .deploy_git/*
fi
# Deploy to GitHub and aliyun
cp -r _book/* .deploy_git/
cd .deploy_git
git add .
COMMIT=`date "+%F %T"`
TAG=`date '+%s'`
git commit -m "Travis CI Site updated: $COMMIT"
git push -f origin gh-pages
git tag | tail -10
git tag
git tag $TAG
git push origin $TAG
