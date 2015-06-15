#!/usr/bin/env bash

set -e

ODL=$1

for i in `seq 1 $NUM_NODES`; do
  hostname="sfc"$i
  echo $hostname
  vagrant ssh $hostname -c "sudo -E /vagrant/infrastructure_launch.py"
done
 

