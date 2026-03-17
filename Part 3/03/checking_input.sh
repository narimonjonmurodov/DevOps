#!/bin/bash

REQUIREMENT() {
  echo "The script is run with 4 parameters. The parameters are numeric. From 1 to 6, for example:"
  echo "script03.sh 1 3 4 5"
  echo "Colour designations: (1 - white, 2 - red, 3 - green, 4 - blue, 5 - purple, 6 - black)"
  echo "The font and background colours of one column must not match!"
}

CHECK() {

if [[ $# -ne 4 ]]; then
  echo "Instruction:"
  REQUIREMENT
  return 1
fi

for param in "$@"
do
  if ! [[ $param =~ ^[1-6]$ ]]; then
    echo "Error: The parameters should be numeric. From 1 to 6. Please run the script again."
    return 1
    fi
done

if [[ $1 -eq $2 || $3 -eq $4 ]]; then
  echo "Error: The font and background colours of one column must not match. Please run the script again."
  return 1
fi

}
