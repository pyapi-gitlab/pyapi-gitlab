#!/bin/sh
# install dependencies
sudo apt-get update -qq
sudo apt-get install -y git-core
# install ruby
curl -sSL https://get.rvm.io | bash -s stable --ruby
gem install bundler
# install git user
sudo adduser --disabled-login --gecos 'GitLab' git
# install mysql
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y mysql-server mysql-client libmysqlclient-dev
mysql --version
mysql -u root -e "CREATE USER 'git'@'localhost' IDENTIFIED BY 'git';"
mysql -u root -e "SET storage_engine=INNODB; CREATE DATABASE IF NOT EXISTS gitlabhq_production DEFAULT CHARACTER SET 'utf8' COLLATE 'utf8_unicode_ci';"
mysql -u root -e "GRANT SELECT, LOCK TABLES, INSERT, UPDATE, DELETE, CREATE, DROP, INDEX, ALTER ON gitlabhq_production.* TO 'git'@'localhost';"


