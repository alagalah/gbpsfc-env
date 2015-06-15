#!/usr/bin/env bash

set -e
hostnum=${HOSTNAME#"sfc"}
sw="sw$hostnum"

sudo ovs-vsctl add-br $sw
for i in `seq 1 5`; do
  sudo ovs-ofctl add-flow $sw "priority=1000,nsp=$i,nsi=255 actions=move:NXM_NX_NSH_C1[]->NXM_NX_NSH_C1[],move:NXM_NX_NSH_C2[]->NXM_NX_NSH_C2[],move:NXM_NX_TUN_ID[0..31]->NXM_NX_TUN_ID[0..31],load:0xC0A83247->NXM_NX_TUN_IPV4_DST[],set_nsi:254,set_nsp:0x1,IN_PORT" -OOpenFlow13

  ovs-ofctl add-flow $sw "priority=1000,nsp=$i,nsi=254 actions=move:NXM_NX_NSH_C1[]->NXM_NX_NSH_C1[],move:NXM_NX_NSH_C2[]->NXM_NX_NSH_C2[],move:NXM_NX_TUN_ID[0..31]->NXM_NX_TUN_ID[0..31],load:0xC0A83247->NXM_NX_TUN_IPV4_DST[],set_nsi:253,set_nsp:0x1,IN_PORT" -OOpenFlow13
done

