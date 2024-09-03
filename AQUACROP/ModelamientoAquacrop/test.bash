#!/bin/bash

var=$2
crop=`awk "NR==$var" cultivos.txt`
echo $crop
xterm -hold -e python3.6 PythonAquacropRun_2.py agent1 $crop  22-03-2018 $1&
sleep 5
xterm -hold -e python3.6 PythonAquacropRun_2.py 0 $crop  22-03-2018 $1
