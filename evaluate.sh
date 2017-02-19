#!/bin/bash

model_file=$(cd "$(dirname "$1")"; pwd)/$(basename "$1")
output=${model_file%%.*}"_results.txt"

./evaluation/run.sh $model_file $output