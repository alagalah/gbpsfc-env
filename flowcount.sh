#!/usr/bin/env bash

hostnum=${HOSTNAME#"gbpsfc"}
sw="sw$hostnum"
set -e
if [ "$1" ]
then
        echo "GROUPS:";
        ovs-ofctl dump-groups $sw -OOpenFlow13; 
        echo;echo "FLOWS:";ovs-ofctl dump-flows $sw -OOpenFlow13 table=$1 --rsort=priority
	echo
	printf "Flow count: "
	ovs-ofctl dump-flows $sw -OOpenFlow13 table=$1 | wc -l
else
        printf "No table entered. $sw flow count: ";
        ovs-ofctl dump-flows $sw -OOpenFlow13 | wc -l
        printf "\nTable0: PortSecurity:  "; ovs-ofctl dump-flows $sw -OOpenFlow13 table=0| wc -l
        printf "\nTable1: IngressNat:    "; ovs-ofctl dump-flows $sw -OOpenFlow13 table=1| wc -l
        printf "\nTable2: SourceMapper:  "; ovs-ofctl dump-flows $sw -OOpenFlow13 table=2| wc -l
        printf "\nTable3: DestMapper:    "; ovs-ofctl dump-flows $sw -OOpenFlow13 table=3| wc -l
        printf "\nTable4: PolicyEnforcer:"; ovs-ofctl dump-flows $sw -OOpenFlow13 table=4| wc -l
        printf "\nTable5: EgressNAT:     "; ovs-ofctl dump-flows $sw -OOpenFlow13 table=5| wc -l
        printf "\nTable6: External:      "; ovs-ofctl dump-flows $sw -OOpenFlow13 table=6| wc -l
fi

