#!/bin/sh
sudo apt-get update
sudo apt-get install openssh-server sendmail
wget https://downloads-packages.s3.amazonaws.com/ubuntu-12.04/gitlab_7.4.2-omnibus-1_amd64.deb
sudo dpkg -i gitlab_7.4.2-omnibus-1_amd64.deb
echo 'external_url "http://localhost:8080"' | sudo tee /etc/gitlab/gitlab.rb
sudo gitlab-ctl reconfigure
