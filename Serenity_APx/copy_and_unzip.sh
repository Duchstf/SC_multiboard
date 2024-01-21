#!/bin/bash
PATTERN_PATH=/data/dhoang/correlator-common/patternfiles


N=83

for i in $(seq 0 $N)
do  
    # Copy things over
    # cp ${PATTERN_PATH}/l1BarrelPhi{1,2,3}-outputs_${i}.txt.gz CL1_Serenity_outputs/
    # cp ${PATTERN_PATH}/l1{HF,HGCal}{Pos,Neg}-outputs_${i}.txt.gz CL1_Serenity_outputs/
    # cp ${PATTERN_PATH}/l1HGCalNoTK-outputs_${i}.txt.gz CL1_Serenity_outputs/
    # l1HGCalNoTK-outputs_29.txt
done

#Untar them
gzip -d CL1_Serenity_outputs/*.txt.gz