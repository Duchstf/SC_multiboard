N=1

for i in $(seq 0 $N)
do
    sh pattern_test.sh \
     sparrow4-linux \ 
     Rx_config.txt \ 
     Tx_config.txt \ 
     ../CL2_APx_inputs/l2_apx_SC_inputs_$i.txt \
     ../CL2_APx_outputs/l2_apx_SC_output_$i.txt.txt 0 0
done