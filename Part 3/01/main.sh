#!/bin/bash

if [ $# -ne 1 ]
then
echo "invalid input"
elif [[ $1 =~ ^[0-9]+$ ]]
then
echo "invalid input"
else
echo "$1"
fi
