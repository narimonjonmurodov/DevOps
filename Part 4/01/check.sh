#!/bin/bash
source "$(dirname $0)/requirements.sh"

CHECK() {
info="Please run $(dirname $0)/main.sh --help for extra info"
if [[ $# -eq 1 && $1 == "--help" ]]
then
  REQUIREMENTS
  return 1
elif [ $# -ne 6 ]
then
  echo -e "Error:  The script is run with 6 parameters !\n$info"
  return 1
elif ! ( [[ $1 =~ ^/ ]] && [ -d $1 ] && [ -w $1 ] )
then
  echo -e "Error(1-parametr): the path(dir) should be absolute, and should be exit, and should be writable!\n$info"
  return 1
elif ! [[ $2 =~ ^[1-9][0-9]*$ ]]
then
  echo -e "Error(2-parametr): should be number!\n$info"
  return 1
elif ! [[ $3 =~ ^[A-Za-z]{1,7}$ ]]
then
  echo -e "Error(3-parametr): no more than 7 characters(A-Za-z)!\n$info"
  return 1
elif ! [[ $4 =~ ^[1-9][0-9]*$ ]]
then
  echo -e "Error(4-parametr): should be number!\n$info"
  return 1
elif ! [[ $5 =~ ^[A-Za-z]{1,7}\.[A-Za-z]{1,3}$ ]]
then
  echo -e "Error(5-parametr): no more than 7 characters(A-Za-z) for the name, no more than 3 characters(A-Za-z) for the extension!\n$info"
  return 1
elif ! ( [[ ${6: -2} == "KB" ]] && [[ ${6:: -2} =~ ^(100|[0-9]?[0-9])$ ]] &&  [[ ${6:: -2} -ne 0 ]] )
then
  echo -e "Error(6-parametr): in kilobytes(KB), but not more than 100!\n$info"
  return 1
fi
}
