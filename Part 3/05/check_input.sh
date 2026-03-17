#!/bin/bash

CHECK() {
if [ $# -ne 1 ]
then
echo "Error: The script is run with a single parameter. For example:"
echo "script05.sh /var/log/"
return 1

elif ! [[ $1 =~ "/"$ ]]
then
echo "Error: The parameter must end with '/'. For example:"
echo "script05.sh /var/log/"
return 1

elif ! [ -d $1 ]
then
echo "Error: The $1 directory does not exist, please enter exist directory !"
return 1
fi
}

