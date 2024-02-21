#Set the bitfile path
bitfile=/scratch/dhoang/SC_multiboard/APx_APx/bitfiles/SC_APd1_v2.bit

#Program the FPGA
apx-prime -H localhost -c config.ini -s "device fpga.bitfile=$bitfile"

#Loop through everything
N=9

#Make output directory
mkdir -p ../CL2_APx_outputs

#Run the FPGA
for i in $(seq 0 $N)
do
    sh pattern_test.sh \
    sparrow5-linux \
    Rx_config.txt \
    Tx_config.txt \
    ../CL2_APx_inputs/CL2_input_$i.txt \
    ../CL2_APx_outputs/CL2_input_$i.txt 0 0
done
