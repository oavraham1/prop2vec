#!/bin/bash

model=$(cd "$(dirname "$1")"; pwd)/$(basename "$1")
output=${model%%.*}"_results.txt"

(cd evaluation; ./run.sh $model $output)