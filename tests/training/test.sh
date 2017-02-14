#!/bin/bash

input="input"
output="output.tmp"
ref="ref"

./../../training/train.sh $input $output
cmp --silent $ref $output || echo "training output has changed"