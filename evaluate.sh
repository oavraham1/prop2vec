#!/bin/bash

model=$(cd "$(dirname "$1")"; pwd)/$(basename "$1")
output=${model%%.*}"_results.txt"

./evaluation/run.sh $model $output