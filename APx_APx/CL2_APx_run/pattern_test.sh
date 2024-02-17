dut=$1
in_cfg=$2
out_cfg=$3
in_data=$4
out_data=$5
rstDly=$6
startDly=$7

echo "Configure Rx buffers for playback mode and load pattern data..."
apx-fs-util buf_operation start $in_cfg $in_data

echo "Configure algo reset and start delay and initiate sequence..."
apx-fs-util algo_reset_delay $rstDly
apx-fs-util algo_start_delay $startDly
apx-fs-util algo_reset cycle

echo "Configure Tx buffers for capture mode..."
apx-fs-util buf_operation start $out_cfg
echo "Dump Tx buffer data..."
apx-fs-util buf_dump T0-99 > $out_data;
