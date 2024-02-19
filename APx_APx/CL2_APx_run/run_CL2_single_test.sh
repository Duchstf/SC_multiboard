#Set the bitfile path
bitfile=/scratch/dhoang/SC_multiboard/APx_APx/bitfiles/SC_APd1_v2.bit

#Program the FPGA
apx-prime -H localhost -c config.ini -s "device fpga.bitfile=$bitfile"

#Make output directory
mkdir -p ../CL2_APx_outputs

#Run the FPGA
sh pattern_test.sh \
sparrow5-linux \
Rx_config.txt \
Tx_config.txt \
../CL2_APx_inputs/CL2_input_0.txt \
../CL2_APx_outputs/CL2_output_0.txt 0 0
