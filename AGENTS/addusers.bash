#!/bin/bash
echo -n "" > list.txt
for (( c=1; c<=$1; c++ ))
do
	sudo prosodyctl register agent$c localhost agent$c$(($c+1))$(($c+2))   
	echo "agent$c@localhost" >> list.txt

done

