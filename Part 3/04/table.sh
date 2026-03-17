#!/bin/bash

TABLE() {
default=(0 default default default default default default )
colour=(0 white red green blue purple black)
c_numbers=(0 1 2 3 4 5 6)
if [ $# -eq 4 ]
then
c_code=("${c_numbers[@]}")
else
c_code=("${default[@]}")
fi

echo ""
echo "Column 1 background = ${c_code[$1]} (${colour[$1]})"
echo "Column 1 font color = ${c_code[$2]} (${colour[$2]})"
echo "Column 2 background = ${c_code[$3]} (${colour[$3]})"
echo "Column 2 font color = ${c_code[$4]} (${colour[$4]})"
}

