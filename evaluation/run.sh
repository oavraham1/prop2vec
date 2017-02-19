#!/bin/bash

script_dir=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
ag_dir=$script_dir/ag-evaluation
eval_file=$script_dir/evaluate.py

if [ ! -d "${ag_dir}" ]
then
  wget -c https://github.com/oavraham1/ag-evaluation/archive/master.zip
  unzip "master.zip" && rm "master.zip"
  mv ag-evaluation-master "${ag_dir}"
fi

python $eval_file $1 > $2