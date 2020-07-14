FROM node:14.4.0-alpine

ENV TZ=Asia/Shanghai

WORKDIR /srv/gitbook

COPY book.json book.json

COPY docker-entrypoint.sh /usr/local/bin/

RUN set -x && apk add --no-cache \
          tzdata \
      && npm install -g gitbook-cli \
      && gitbook install \
      && ln -s /usr/local/bin/docker-entrypoint.sh / \
      && rm -rf /root/.npm /tmp/*

EXPOSE 4000

VOLUME /srv/gitbook-src

WORKDIR /srv/gitbook-src

ENTRYPOINT ["docker-entrypoint.sh"]

CMD server
