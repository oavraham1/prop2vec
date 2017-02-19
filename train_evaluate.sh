#!/bin/bash

props="w"
corpus_processed=$(cd "$(dirname "$1")"; pwd)/$(basename "$1")
model_path=${corpus_processed}_$props
model_full_path=$model_path.vec

script_dir=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
training_dir=$script_dir/training
exe_name=fasttext

(cd $training_dir; [ -e $exe_name ] && rm $exe_name; make; ./$exe_name skipgram -input $corpus_processed -output $model_path -props $props -lr 0.025 -dim 200 -ws 2 -epoch 5 -minCount 5 -neg 5 -loss ns -bucket 2000000 -thread 1 -t 1e-3 -lrUpdateRate 100)

./evaluate.sh $model_full_path