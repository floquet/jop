$KEYS dir

echo off
message ''
message 'The next set of commands reads in three files containing'
message 'amplitude responses from three stations and produces an'
message 'overlay plot in LINLOG format.'
message ''
pause message "Press return to continue ..."
echo on

read $dir$mnv_z_am $dir$knb_z_am $dir$elk_z_am
xlim .04 .16
ylim .0001 .006
linlog
title 'Rayleigh Wave Amplitude Spectra for NESSEL'
symbol 2 increment
window 2 x .01 .5 y .45 .9
bw 2
xlabel "Frequency (Hz)"
plot2
saveimg ./results/rayleigh_amp.pdf
echo off
pause message "Press return to continue ..."

echo off
symbol off
title off
xlim off
ylim off
linlin
echo off
message ''
message 'The next set of commands reads part of a signal around the'
message 'first arrival time, takes its FFT, and then plots the signal'
message 'and its amplitude response in both LINLOG and LOGLOG format.'
message ''
pause message "Press return to continue ..."

echo on
cut a -0.1 n 512
read $dir$cdv_z
taper
fft womean amph
writesp $dir$temp

read
title 'SEISMIC TRACE'
fileid off
window 3 x .04 .53 y .48 .93
bw 3
begfr
xvport .1 .9
yvport .7 .9
qdp off
linlin
xlabel 'Time (sec)'
plot
yvport .15 .55
xvport .1 .45
linlog
cut off
read $dir$temp.am
title 'Amplitude Response [linlog]'
ylim 1e-5 1
xlabel "Frequency (Hz)"
plot
xvport .55 .9
loglog
title 'Amplitude Response [loglog]'
xlim 1 60
plot
endframe
saveimg ./results/3-plots.pdf

echo off
pause message "Press return to continue ..."
title off
xlim off
xlabel off
linlin
ylim off
qdp on
xvport .1 .9
yvport .15 .9
