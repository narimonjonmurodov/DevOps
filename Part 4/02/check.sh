#!/bin/bash
source "$(dirname $0)/requirements.sh"

CHECK() {
info="Please run $(dirname $0)/main.sh --help for extra info"
if [[ $# -eq 1 && $1 == "--help" ]] && [ $# -eq 1 ]
then
  REQUIREMENTS
  return 1
elif [ $# -ne 3 ]
then
  echo -e "Error:  The script is run with 3 parameters !\n$info"
  return 1
elif ! [[ $1 =~ ^[A-Za-z]{1,7}$ ]]
then
  echo -e "Error(1-parametr): no more than 7 characters(A-Za-z)!\n$info"
  return 1
elif ! [[ $2 =~ ^[A-Za-z]{1,7}\.[A-Za-z]{1,3}$ ]]
then
  echo -e "Error(2-parametr): no more than 7 characters(A-Za-z) for the name, no more than 3 characters(A-Za-z) for the extension!\n$info"
  return 1
elif ! ( [[ ${3: -2} == "MB" ]] && [[ ${3:: -2} =~ ^(100|[0-9]?[0-9])$ ]] &&  [[ ${3:: -2} -ne 0 ]] )
then
  echo -e "Error(3-parametr): in kilobytes(MB), but not more than 100!\n$info"
  return 1
else
  space=$(df -k / | awk 'NR==2 {print $4}')
  if [ $space -le 1048576 ]
  then
    echo "Error: Less than 1GB of free space left in / partition!"
    return 1
  fi
fi
}
