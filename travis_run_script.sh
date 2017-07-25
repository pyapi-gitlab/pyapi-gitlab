#!/usr/bin/env bash
if $INTEGRATION_TEST -eq 1; then
    docker-compose -f docker/v93/docker-compose.yml build
    docker-compose -f docker/v93/docker-compose.yml up --abort-on-container-exit
    ./cov
else
    pip install -Ur test-requirements.txt
    ./cov
fi
