# Bash script for running linters to check through python code.

# Required input:
# - File name

#!/bin/bash
if [ $# -ne 1 ]; then
  echo "Error: You did not enter only one document name, please try again." > stderr
  exit 1
elif [ ! -f "$1" ]; then
  echo "Error: file does not exist" > stderr
  exit 1
elif [ -d "$1" ]; then
  echo "Error: file name is a directory" > stderr
  exit 1
else
  echo "PyCodeStyle:"
  pycodestyle $1
  echo "PyDocStyle:"
  pydocstyle $1
  echo "Pylint:"
  pylint $1
  exit 0
fi
