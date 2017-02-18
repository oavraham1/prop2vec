#!/bin/bash

ref=$PWD/results.txt
input=ag-evaluation/model.vec
output=$PWD/results.tmp

(cd "../../evaluation"; ./run.sh $input $output)
cmp --silent $ref $output || echo "evaluation output has changed"