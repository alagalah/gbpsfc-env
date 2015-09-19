#!/usr/bin/env bash

set -e
if [ -f "demo.lock" ] ; then
  cat "demo.lock"
fi

for i in `seq 1 $NUM_NODES`; do
  hostname="gbpsfc"$i
  switchname="sw"$i
  echo $hostname
  vagrant ssh $hostname -c "sudo ovs-vsctl show;sudo ovs-ofctl dump-flows $switchname -OOpenFlow13 | wc -l"

done
 
