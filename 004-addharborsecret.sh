#!/bin/bash

source .env

ku create secret docker-registry ${HARBOR_SECRET} --from-file=.dockerconfigjson=$HOME/.docker/config.json