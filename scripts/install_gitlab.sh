#!/bin/bash
# install gitlab
cd /home/git
sudo -u git -H git clone --depth=1 https://gitlab.com/gitlab-org/gitlab-ce.git -b 7-2-stable gitlab
cd /home/git/gitlab
sudo -u git -H cp config/gitlab.yml.example config/gitlab.yml
sudo chown -R git log/
sudo chown -R git tmp/
sudo chmod -R u+rwX log/
sudo chmod -R u+rwX tmp/
sudo -u git -H mkdir /home/git/gitlab-satellites
sudo chmod u+rwx,g=rx,o-rwx /home/git/gitlab-satellites
sudo chmod -R u+rwX tmp/pids/
sudo chmod -R u+rwX tmp/sockets/
sudo chmod -R u+rwX  public/uploads
sudo -u git -H cp config/unicorn.rb.example config/unicorn.rb
sudo -u git -H cp config/initializers/rack_attack.rb.example config/initializers/rack_attack.rb
sudo -u git -H git config --global user.name "GitLab"
sudo -u git -H git config --global user.email "example@example.com"
sudo -u git -H git config --global core.autocrlf input
sudo -u git -H sh -c "cat config/database.yml.mysql | sed 's/password: \".*\"/password: "git"/g' > config/database.yml"
sudo -u git -H chmod o-rwx config/database.yml
bundle -v
sudo -u git -H bundle install --deployment --without development test postgres aws
# install gitlab shell
sudo -u git -H bundle exec rake gitlab:shell:install[v1.9.7] REDIS_URL=redis://localhost:6379 RAILS_ENV=production


