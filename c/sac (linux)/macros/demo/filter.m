* Directory variable for macro, specified during invocation
$KEYS dir

echo off
message ''
message 'This example applies a bank of IIR filters to a signal and'
message 'then plots the result using one of the SAC canned plot formats.'
message 'It creates a series of temporary data files in the process.'
message 'The temporary files are deleted at the end of the macro.'
message ''
echo on

read $dir$elk_z
chnhdr kevnm broadband
write $dir$temp0

lowpass npoles 3 corner .177 passes 2
decimate 6
chnhdr kevnm 'Band: .000 .177'
write $dir$temp1

read $dir$temp0
bandpass npoles 3 corner .177 .354 passes 2
decimate 4
chnhdr kevnm 'Band: .177 .354'
write $dir$temp2

read
bandpass corner .354 .707
decimate 2
chnhdr kevnm 'Band: .354 .707'
write $dir$temp3

read
bandpass corner .707 1.41
chnhdr kevnm 'Band: .707 1.41'
write $dir$temp4

read
bandpass corner 1.41 2.83
chnhdr kevnm 'Band: 1.41 2.83'
write $dir$temp5

* Plot the results
read $dir$temp0 $dir$temp1 $dir$temp2 $dir$temp3 $dir$temp4 $dir$temp5
xlabel 'Time (sec)'
title size medium 'Bandpass-Partitioned Signals'
ylim all
qdp off
xlim 50 200
fileid on type list kevnm
bw 4
plot1
saveimg ./results/bandpass_signals.pdf

echo off
pause message "Press return to continue ..."
title off
xlabel off
xlim off
ylim off
fileid type default
qdp on
echo on
sc \rm $dir$temp*
