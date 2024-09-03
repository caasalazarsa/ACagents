#!/bin/bash
trap 'R=true;echo "Caught SIGINT"' SIGINT
setsid xterm &
while : ; do
    R=false
    wait
    [ $R == false ] && break
done

