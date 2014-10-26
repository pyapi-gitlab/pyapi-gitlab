#!/bin/bash
# install gitlab
cd 
git clone --depth=1 https://gitlab.com/gitlab-org/gitlab-ce.git -b 7-2-stable gitlab
cd /home/travis/gitlab
sh -c "cat config/gitlab.yml.example | sed 's/port: 80/port: 8080/g' > config/gitlab.yml"
chmod -R u+rwX log/
chmod -R u+rwX tmp/
mkdir /home/travis/gitlab-satellites
chmod u+rwx,g=rx,o-rwx /home/travis/gitlab-satellites
chmod -R u+rwX tmp/pids/
chmod -R u+rwX tmp/sockets/
chmod -R u+rwX public/uploads
cp config/unicorn.rb.example config/unicorn.rb
cp config/initializers/rack_attack.rb.example config/initializers/rack_attack.rb
git config --global user.name "GitLab"
git config --global user.email "example@example.com"
git config --global core.autocrlf input
sh -c "cat config/database.yml.mysql | sed 's/password: \".*\"/password: "git"/g' > config/database.yml"
chmod o-rwx config/database.yml
bundle install --deployment --without development test postgres aws
bundle install --deployment --without development test postgres aws
# install gitlab shell
bundle exec rake gitlab:shell:install[v1.9.7] REDIS_URL=redis://localhost:6379 RAILS_ENV=production
echo "yes" |bundle exec rake gitlab:setup RAILS_ENV=production
cp lib/support/init.d/gitlab /etc/init.d/gitlab
update-rc.d gitlab defaults 21
bundle exec rake gitlab:env:info RAILS_ENV=production
bundle exec rake assets:precompile RAILS_ENV=production
service gitlab restart
bundle exec rake gitlab:check RAILS_ENV=production

