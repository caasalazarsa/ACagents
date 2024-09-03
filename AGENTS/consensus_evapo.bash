#!/bin/bash

xterm -hold -e python3.6 coordinationagent.py agent$1@localhost agent$1$(($1+1))$(($1+2)) $3 & sleep 5
for (( c=1; c<=$(($1-2)); c++ ))
do
	var=$((1 + $RANDOM % 6))
	crop=`awk "NR==$var" cultivos.txt`
	echo $crop	
	xterm -hold -e python3.6 evapotranspirationagent.py agent$c@localhost agent$c$(($c+1))$(($c+2)) $crop 1 22-03-2018 1 1 Bogota.ETo Boyaca.PLU $2 & sleep 1
done
var=$((1 + $RANDOM % 6))
crop=`awk "NR==$var" cultivos.txt`
echo $crop
xterm -hold -e python3.6 evapotranspirationagent.py  agent$(($1-1))@localhost agent$(($1-1))$1$(($1+1)) $crop 1 22-03-2018 1 1 Bogota.ETo Boyaca.PLU $2 & sleep 1

echo "Press [CTRL+C] to stop.."
while true
do
	
	sleep 1
done




