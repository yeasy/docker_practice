Docker —— From start to practice
================================

v0.3.2

[Docker](docker.com) is a great project, it completely releases the power of virtualization, cloud computing greatly reducing the cost of supply of resources,
while allowing test deploy and distribution of applications both more efficient and easier than ever!

This book wants to give basic knowledge to Linux Docker beginners, but also hope to serve as reference to the principles and advanced users implementation.
At the same time, the book gives practical cases, available for reference during actual deployment. The first six chapters content explains
the basic concepts of Docker and operation;
Chapters 7 to 9 introduce some advanced operations;
Chapter 10 shows a typical application scenarios and practical cases;
Chapters 11 to 13 are on related technologies that power Docker.
Chapter 14 introduces some related open source projects.

Online reading: [GitBook](https://www.gitbook.io/book/yeasy/docker_practice/en)
or [DockerPool](http://dockerpool.com/static/books/docker_practice/en/index.html).

You are welcome on the DockerPool community microblogging [@dockerpool](http://weibo.com/u/5345404432), or to join DockerPool QQ group (341410255),
to share Docker resources, and exchange on Docker technology.

![Docker technology introduction and practical](docker_primer.png)

《[Practical start to Docker technology](http://item.jd.com/11598400.html)》 book(ZH) has been officially published,
covering a large number of practical cases, which you are welcome to read.

* [China-Pub](http://product.china-pub.com/3770833)
* [Jingdong books](http://item.jd.com/11598400.html)
* [Dangdang books](http://product.dangdang.com/23620853.html)
* [Amazon Books](http://www.amazon.cn/%E5%9B%BE%E4%B9%A6/dp/B00R5MYI7C/ref=lh_ni_t?ie=UTF8&psc=1&smid=A1AJ19PSB66TGU)

## Main Version History
* 0.4: 2015-01-TBD
    * Add Etcd project
    * Add Fig Project
* 0.3: 2014-11-25
    * Complete repository section;
    * Rewrite security chapter;
    * Fixed sections of the underlying implementation architecture, namespace, the control group, the file system, the contents of the container format;
    * Add a description of the common repository and images;
    * Add Dockerfile introduction ;
    * English-text format revision again.
    * Revised written expression.
    * Traditional version release branch: zh-Hant.
* 0.2: 2014-09-18
    * Official documentation rewrite introduce basic concepts, installation, mirror, container, storage, data management, networking and other chapters;
    * Add the underlying implementation chapter;
    * Add a command to query and resource links section;
    * Other amendments.
* 0.1: 2014-09-05
    * Add basic content;
    * Corrected typos and expression.


The source of book is managed on Github, you are welcome to participate: [https://github.com/yeasy/docker_practice](https://github.com/yeasy/docker_practice).
[Contributors list](https://github.com/yeasy/docker_practice/graphs/contributors).

## Contributors steps
* On GitHub, `fork` to your own repository, as `user/docker_practice`, then `clone` to a local repo, and set user information.
```
$ git clone git@github.com:user/docker_practice.git
$ cd docker_practice
$ git config user.name "yourname"
$ git config user.email "your email"
```
* After modifying the code, to submit, push to your repository.
```
$ #do some change on the content
$ git commit -am "Fix issue #1: change helo to hello"
$ git push
```
* Submit pull request on GitHub.
* Regular use of your repository to keep updateed from the upstream respository.
```
$ git remote add upstream https://github.com/yeasy/docker_practice
$ git fetch upstream
$ git checkout master
$ git rebase upstream/master
$ git push -f origin master
```

[Summary](SUMMARY.md)
