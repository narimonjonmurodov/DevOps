#!/bin/bash

REQUIREMENTS() {
echo "Usage: ./main.sh <method>"
echo ""
echo "Methods:"
echo "  1  Delete files/folders listed in the log file (from Part 2)"
echo "  2  Delete files/folders by creation date/time"
echo "     - Enter start and end as YYYY-MM-DD HH:MM"
echo "  3  By name mask (i.e. characters, underlining and date)."
echo ""
echo "Example:"
echo "  $1 1"
}

CHECK() {
script="$(dirname $0)/main.sh"
info="Please run $script --help  for extar info!"
if [[ $1 == "--help" ]] && [ $# -eq 1 ]
then
  REQUIREMENTS $script
  return 1
elif [ $# -ne 1 ]
then
  echo "Error: Script run with one parametr!"
  echo $info
  return 1
elif ! [[ $1 =~ ^[1-3]$ ]]
then
  echo "Error(1st parametr): it should be in range [1-3]."
  echo $info
  return 1
fi
}
