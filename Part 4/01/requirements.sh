#!/bin/bash

REQUIREMENTS() {
echo "The script is run with 6 parameters. An example of running a script:"
echo "$(dirname $0)/main.sh /opt/test 4 az 5 az.az 3KB"
echo ""
echo "Parameter 1 is the absolute path."
echo "Parameter 2 is the number of subfolders."
echo "Parameter 3 is a list of English alphabet letters used in folder names (no more than 7 characters)."
echo "Parameter 4 is the number of files in each created folder."
echo "Parameter 5 — the list of English alphabet letters used in the file name and extension (no more than 7 characters for the name, no more than 3 characters for the extension)."
echo "Parameter 6 — file size (in kilobytes(KB), but not more than 100)."
}

