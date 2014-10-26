#!/bin/sh
# install dependencies
#sudo apt-get update -qq
# sudo apt-get install -y build-essential zlib1g-dev libyaml-dev libssl-dev libgdbm-dev libreadline-dev libncurses5-dev libffi-dev curl openssh-server redis-server checkinstall libxml2-dev libxslt-dev libcurl4-openssl-dev libicu-dev logrotate python-docutils pkg-config cmake
#sudo apt-get install -y build-essential zlib1g-dev libyaml-dev libssl-dev libgdbm-dev libreadline-dev libncurses5-dev libffi-dev curl openssh-server checkinstall libxml2-dev libxslt-dev libcurl4-openssl-dev libicu-dev logrotate python-docutils pkg-config cmake
sudo apt-get install -y git-core
#git --version
# install ruby
#sudo apt-get remove -y ruby1.8 libruby1.8 libruby1.9.1
#mkdir /tmp/ruby && cd /tmp/ruby
#curl -L --progress ftp://ftp.ruby-lang.org/pub/ruby/2.1/ruby-2.1.2.tar.gz | tar xz
#cd ruby-2.1.2
#./configure --disable-install-rdoc
#make
#sudo make install
#curl -sSL https://get.rvm.io | sudo bash -s stable --ruby
#source /home/travis/.rvm/scripts/rvm
#sudo gem install bundler --no-ri --no-rdoc
# install git user
sudo adduser --disabled-login --gecos 'GitLab' git
# install mysql
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y mysql-server mysql-client libmysqlclient-dev
mysql --version
mysql -u root -e "CREATE USER 'git'@'localhost' IDENTIFIED BY 'git';"
mysql -u root -e "SET storage_engine=INNODB; CREATE DATABASE IF NOT EXISTS gitlabhq_production DEFAULT CHARACTER SET 'utf8' COLLATE 'utf8_unicode_ci';"
mysql -u root -e "GRANT SELECT, LOCK TABLES, INSERT, UPDATE, DELETE, CREATE, DROP, INDEX, ALTER ON gitlabhq_production.* TO 'git'@'localhost';"


