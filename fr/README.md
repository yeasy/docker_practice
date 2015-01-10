Docker —— De l'introduction à la pratique
=========================================

v0.3.2

Docker est un projet génial, il offre toute la puissance de la virtualisation, le cloud computing permet de réduire considérablement
le coût d'utilisation de mise à dispostion des ressources, tout en permettant de tester, déployer et distribuer des applications réparties
de manière efficace et plus simplement qu'auparavant.

Ce livre a pour but d'offrir les connaissance de base nécessaires aux débutants sous Docker, mais espère aussi permettre de comprendre des principes
et des cas de mise en œuvre plus avancés. Le livre donne des cas pratiques comme référence pour déploiement réel.
Les six premiers chapitres ont pour but de permettre au lecteur de comprendre les concepts de base de Docker et son fonctionnement;
Les chapitre 7 à 9 présentent plusieurs opérations avancées;
Le Chapitre 10 montre des scénarios typiques d'utilisation d'application et cas pratiques;
Les chapitres 11 à 13 présentent des technologies connexes qui propulsent Docker.
Le chapitre 14 présente certains projets open source connexes.

Lecture en ligne: [GitBook](https://www.gitbook.io/book/yeasy/docker_practice/fr) ou [DockerPool](http://dockerpool.com/static/books/docker_practice/fr/index.html).

Vous êtes bienvenue sur la communauté de microblogging DockerPool(ZH), dédiée à Docker, [@dockerpool](http://weibo.com/u/5345404432),
ou à rejoindre le groupe(ZH) DockerPool QQ (341410255), pour partager des ressources et échanger sur les technologies Docker.

![Docker De l'introduction à la pratique](docker_primer.png)

Le livre 《[Docker De l'introduction à la pratique](http://item.jd.com/11598400.html)》a été publié officiellement(ZH), couvrant un grand nombre de cas réels,
que vous êtes invité à lire.

* [China-Pub](http://product.china-pub.com/3770833)
* [Livres Jingdong](http://item.jd.com/11598400.html)
* [Livres Dangdang](http://product.dangdang.com/23620853.html)
* [Livres Amazon](http://www.amazon.cn/%E5%9B%BE%E4%B9%A6/dp/B00R5MYI7C/ref=lh_ni_t?ie=UTF8&psc=1&smid=A1AJ19PSB66TGU)

## Historique de la version principale
* 0.4: 2015-01-TBD
    * Ajout projet ETCD
    * Ajout projet Fig
* 0.3: 2014-11-25
    * Remplir la section de l'entrepôt;
    * Réécrire chapitre Sécurité;
    * Sections sur l'architecture interne, espace de noms, les cgroups, le système de fichier, le format de conteneur;
    * Ajout entrepôt et images communs;
    * Ajouter introduction sur les Dockerfile;
    * Nouvelle version format texte Anglais.
    * Expression écrite révisée.
    * Branche chinois traditionnel version finale: zh-Hant.
* 0.2: 2014-09-18
    * Réécriture documentation officielle introduire les concepts de base, l'installation, image, conteneur, le stockage, la gestion des données,
    réseau et d'autres chapitres;
    * Ajout chapitre mise en œuvre interne;
    * Ajout commande à la section requête et ressources sur linking;
    * D'autres ajouts.
* 0.1: 2014-09-05
    * Ajouter le contenu de base;
    * Corrections d'erreurs typographiques et d'expression.

Les sources du livre sont gérées sur Github, vous êtes invité à y contribuer: [https://github.com/yeasy/docker_practice](https://github.com/yeasy/docker_practice).
[Liste collaborateurs](https://github.com/yeasy/docker_practice/graphs/contributors).

## Différentes étapes de contribution
* Faire un `fork` dans votre espace Github `utilisateur/docker_practice`, puis un `clone` en local,
et assurez-vous d'avoir vos informations utilisateur définies:
```
$ git clone git@github.com:utilisateur/docker_practice.git
$ cd docker_practice
$ git config user.name "mon nom"
$ git config user.email "votre email"
```
* Après avoir modifié le code, pou le soumettre, poussez leur vers votre fork:
```
$ #Apportez vos modifications au contenu du livre
$ git commit -am "Fix issue #1: change helo to hello"
$ git push
```
* Faire un pull request sur Github.
* Configurer votre dépôt local pour mettre à jour le contenu par rapport au dépôt original:
```
$ git remote add upstream https://github.com/yeasy/docker_practice
$ git fetch upstream
$ git checkout master
$ git rebase upstream/master
$ git push -f origin master
```

[Résumé](SUMMARY.md)
