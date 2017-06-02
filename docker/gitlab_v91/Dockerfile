FROM docker pull gitlab/gitlab-ce

COPY . /tmp/pyapi-gitlab
RUN apt-get install python3-pip
RUN cd /tmp/pyapi-gitlab && pip3 install -Ur requirements.txt && python -m unittest discover -s integration_tests.tests_v91