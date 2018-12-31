FROM node:alpine as frontend

COPY package.json /app/

RUN cd /app \
      && npm install --registry=https://registry.npm.taobao.org

COPY webpack.mix.js /app/
COPY resources/assets/ /app/resources/assets/

RUN cd /app \
      && npm run production

FROM composer as composer

COPY database/ /app/database/
COPY composer.json /app/

RUN cd /app \
      && composer config -g repo.packagist composer https://packagist.laravel-china.org \
      && composer install \
           --ignore-platform-reqs \
           --no-interaction \
           --no-plugins \
           --no-scripts \
           --prefer-dist

FROM php:7.2-fpm-alpine as laravel

ARG LARAVEL_PATH=/app/laravel

COPY --from=composer /app/vendor/ ${LARAVEL_PATH}/vendor/
COPY . ${LARAVEL_PATH}
COPY --from=frontend /app/public/js/ ${LARAVEL_PATH}/public/js/
COPY --from=frontend /app/public/css/ ${LARAVEL_PATH}/public/css/
COPY --from=frontend /app/mix-manifest.json ${LARAVEL_PATH}/mix-manifest.json

RUN cd ${LARAVEL_PATH} \
      && php artisan package:discover \
      && mkdir -p storage \
      && mkdir -p storage/framework/cache \
      && mkdir -p storage/framework/sessions \
      && mkdir -p storage/framework/testing \
      && mkdir -p storage/framework/views \
      && mkdir -p storage/logs \
      && chmod -R 777 storage

FROM nginx:alpine as nginx

ARG LARAVEL_PATH=/app/laravel

COPY laravel.conf /etc/nginx/conf.d/
COPY --from=laravel ${LARAVEL_PATH}/public ${LARAVEL_PATH}/public
