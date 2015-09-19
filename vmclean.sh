#!/usr/bin/env bash

docker stop -t=1 $(docker ps -a -q) > /dev/null 2>&1
docker rm $(docker ps -a -q) > /dev/null 2>&1

/vagrant/resetOVSDB.sh

ovs-vsctl show

