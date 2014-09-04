#!/bin/sh
export DEBIAN_FRONTEND=noninteractive
sudo apt-get update -qq
sudo apt-get install -y build-essential zlib1g-dev libyaml-dev libssl-dev libgdbm-dev libreadline-dev libncurses5-dev libffi-dev curl openssh-server redis-server checkinstall libxml2-dev libxslt-dev libcurl4-openssl-dev libicu-dev logrotate python-docutils pkg-config cmake
sudo apt-get install -y git-core
git --version
sudo apt-get remove -y ruby1.8
mkdir /tmp/ruby && pushd /tmp/ruby
curl -L --progress ftp://ftp.ruby-lang.org/pub/ruby/2.1/ruby-2.1.2.tar.gz | tar xz
cd ruby-2.1.2
./configure --disable-install-rdoc
make
sudo make install
sudo gem install bundler --no-ri --no-rdoc
sudo apt-get install -y mysql-server mysql-client libmysqlclient-dev
mysql --version
popd