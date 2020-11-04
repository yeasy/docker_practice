## List all Images

If you want to list all the images downloaded, you can use the command `docker image ls` or `docker images`.

```bash
$ docker image ls
REPOSITORY           TAG                 IMAGE ID            CREATED             SIZE
redis                latest              5f515359c7f8        5 days ago          183 MB
nginx                latest              05a60462f8ba        5 days ago          181 MB
mongo                3.2                 fe9198c04d62        5 days ago          342 MB
<none>               <none>              00285df0df87        5 days ago          342 MB
ubuntu               18.04               f753707788c5        4 weeks ago         127 MB
ubuntu               latest              f753707788c5        4 weeks ago         127 MB
```

You can see `Repository`, `Tag`, `Image ID`, `Created` and `Size` from the list.

Among these, the repository name and tag have been introduced in the basic concepts chapter. **Image ID** is the unique identifier for the image, and an image can correspond to multiple **labels**. In the exmaple above, we can see `ubuntu:18:04` and `ubuntu:latest` having the same ID, since they are aliases for the same image.

### Image Size

If you pay close attention to all of these. You may find that the disk space they occupy is different from the one at Docker Hub. For example, `ubuntu:18.04` is `127MB` here, but on [Docker Hub](https://hub.docker.com/r/library/ubuntu/tags/), `50MB` is displayed. That's because what is shown on Docker Hub is the size after compression. During image download and upload, the image is compressed, because the data transfer is the main factor taken into consideration. However, when we use the command `docker image ls`, that's the size after expansion. To be more precisely, the total size after expanding all the layers locally, because we care more about local space occupied when an image is on our disk.

One more thing to note is that in the `docker image ls` list, the total size of images is far less than the actual size. Since the Docker imags are stored in multiple layers, and there are inheritance and reuse, there might be different images using the same basic images and sharing some common layers. As we have mentioned, Docker uses Union FS, we only keep one copy for the same layers, so the actual space occupied is far less than the mere sum.

You can use the following command to see the space utilized by images, containers, data volumes.

```bash
$ docker system df

TYPE                TOTAL               ACTIVE              SIZE                RECLAIMABLE
Images              24                  0                   1.992GB             1.992GB (100%)
Containers          1                   0                   62.82MB             62.82MB (100%)
Local Volumes       9                   0                   652.2MB             652.2MB (100%)
Build Cache                                                 0B                  0B
```

### Dangling Image

In the image list above, we can see a special image, the one without repository name nor tag, all being `<none>`:

```bash
<none>               <none>              00285df0df87        5 days ago          342 MB
```

This image is originally with name and tag(`mongo:3.2`). As the official image being maintained, and the release of new versions, when we execute `docker pull mongo:3.2`, the tag `mongo:3.2` is transferred to the new iamge, and the name on the old image is canceled, end up being `<none>`. Besides, `docker pull`, `docker build` might also cause this phenomemon. Because the new and old image are of the same name, the name of the old image is canceled, thus causing the repository and tag both being `<none>`. These images without tags are also called **dangling images**, we can use the following commands to show them:

```bash
$ docker image ls -f dangling=true
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
<none>              <none>              00285df0df87        5 days ago          342 MB
```

Generally speaking, the dangling images are useless, we can remove them with the following commands with ease:

```bash
$ docker image prune
```

### Intermediate Layer Images

To accelerate the build of images and improve the resource utilization, Docker uses **Intermediate Layer Images**. So after using Docker for a while, you may see a list of intermediate images as dependencies. The default `docker image ls` only shows the top images, if you want to show all the images including intermediate images, you need to add the `-a` paramter.

```bash
$ docker image ls -a
```

You will see a lot of images without tags with this command. Differing from `dangling images`, these untagged images are intermediate layer images, and are what a lot of other images depend on. These untagged images should not be deleted, otherwise, it will cause missing dependencies errors for upstream images. In fact, these images are not necessary to delete, as we have mentioned, the same layers will be only stored once. These images are dependencies for other images, and their existence will not cause any redundancy, you will need them in any way. They will disappear the moment you delete all the images that reference them.

### List Images Partially

Without any parameter, `docker image ls` lists all the top-level images, but sometimes we only want them partially. `docker image ls` has several parameters to help us achieve this goal.

To list images based on repository name.

```bash
$ docker image ls ubuntu
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
ubuntu              18.04               f753707788c5        4 weeks ago         127 MB
ubuntu              latest              f753707788c5        4 weeks ago         127 MB
```

To list a certain image, specifying repository name and label.

```bash
$ docker image ls ubuntu:18.04
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
ubuntu              18.04               f753707788c5        4 weeks ago         127 MB
```

Besides, `docker image ls` supports the `--filter` parameter, or simply `-f`. As we have seen before, using filter to list dangling image, and it has more usages. For example, if we want to see images with edition after `mongo:3.2`, we can use the following command:

```bash
$ docker image ls -f since=mongo:3.2
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
redis               latest              5f515359c7f8        5 days ago          183 MB
nginx               latest              05a60462f8ba        5 days ago          181 MB
```

If we want to see some versions of images before, we can simply replace `since` with `before`.

If we have defined the `LABEL` during the image build, we can also filter with the `LABEL` option.

```bash
$ docker image ls -f label=com.example.version=0.1
...
```

### Show with Specified Format

By default, `docker image ls` will show a full list, but we do not need it all the time. For example, when we delete dangling images, we use `docker image ls` to list all the IDs of dangling images and then pass them over to `docker image rm` as parameters to remove the specified images. Under this circumstance, we can apply the `-q` option.

```bash
$ docker image ls -q
5f515359c7f8
05a60462f8ba
fe9198c04d62
00285df0df87
f753707788c5
f753707788c5
1e0c3dd64ccd
```

`--filter` together with `-q` to generate a ID list in a specified range, and then passing them over to another `docker` command as parameter is a common practice for Docker commands. Not only for images, we will see all this kind of combinations in other kinds of commands, with them, we can achieve great functionalities. So when you see some filters while reading the documents, please pay attention to how they are used in practice.

In some other occasions, we may not be content with the table structure and would like to reorganize the columns. In this case, we can use the [Go Templates](https://gohugo.io/templates/go-templates/).

For example, using the following commands will list the image results, with only image ID and repository names.

```bash
$ docker image ls --format "{{.ID}}: {{.Repository}}"
5f515359c7f8: redis
05a60462f8ba: nginx
fe9198c04d62: mongo
00285df0df87: <none>
f753707788c5: ubuntu
f753707788c5: ubuntu
1e0c3dd64ccd: ubuntu
```

Or we may want to show the table with equal horizontal tabulations and with title, we can define them by ourselves.

```bash
$ docker image ls --format "table {{.ID}}\t{{.Repository}}\t{{.Tag}}"
IMAGE ID            REPOSITORY          TAG
5f515359c7f8        redis               latest
05a60462f8ba        nginx               latest
fe9198c04d62        mongo               3.2
00285df0df87        <none>              <none>
f753707788c5        ubuntu              18.04
f753707788c5        ubuntu              latest
```
