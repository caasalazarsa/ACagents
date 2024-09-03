#!/bin/bash
soil=`awk 'NR==2' soildata_.csv`
echo $soil 
var1=$(echo $soil | cut -f3 -d,)
echo $var1
var11=$(echo $soil | cut -f5 -d,)
echo $var11
dep=`awk 'NR==10' CropData_root_depletion_.csv`
echo $dep
var2=$(echo $dep | cut -f3 -d,)
echo $var2
dep2=`awk 'NR==10' CropData_root_depletion_.csv`
echo $dep2
xterm -hold -e python3.6 coordinationagent.py agent$1@localhost agent$1$(($1+1))$(($1+2)) &
sleep 5
for (( c=1; c<=$(($1-2)); c++ ))
do
	var22=$(echo $dep2 | cut -f3 -d,)	
	xterm -hold -e python3.6 groundsensoragent.py agent$c@localhost agent$c$(($c+1))$(($c+2)) $var1 $var11 $var22 1&
        if [ "$dep2" = "$dep" ];
        then
	  dep2=`awk 'NR==29' CropData_root_depletion_.csv`
        else
          dep2=`awk 'NR==10' CropData_root_depletion_.csv`
        fi
	sleep 1
done
var22=$(echo $dep2 | cut -f3 -d,)
xterm -hold -e python3.6 groundsensoragent.py  agent$(($1-1))@localhost agent$(($1-1))$1$(($1+1)) $var1 $var11 $var22 1	
