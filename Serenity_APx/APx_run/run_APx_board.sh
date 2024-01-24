#Set the bitfile path
bitfile=/scratch/dhoang/SC_multiboard/Serenity_APx/bitfiles/SC_APd1_v2.bit

#Program the FPGA
apx-prime -H localhost -c config.ini -s "device fpga.bitfile=$bitfile"

#Loop through everything
N=83

#Make output directory
mkdir -p ../CL2_APx_outputs

#Run the FPGA
for i in $(seq 0 $N)
do
    sh pattern_test.sh \
    sparrow5-linux \
    Rx_config.txt \
    Tx_config.txt \
    ../CL2_APx_inputs/l2_apx_SC_inputs_$i.txt \
    ../CL2_APx_outputs/l2_apx_SC_output_$i.txt 0 0
done
