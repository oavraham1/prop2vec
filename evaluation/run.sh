#!/bin/bash

AGDIR=ag-evaluation

if [ ! -d "${AGDIR}" ]
then
  wget -c https://github.com/oavraham1/ag-evaluation/archive/master.zip
  unzip "master.zip" && rm "master.zip"
  mv ag-evaluation-master "${AGDIR}"
fi

python evaluate.py $1 > $2