#!/bin/bash

props="w+l+m"
corpus_processed=$1
model_path=${corpus_processed}_$props
model_full_path=$model_path.vec

./training/fasttext skipgram -input $corpus_processed -output $model_path -props $props -lr 0.025 -dim 200 -ws 2 -epoch 5 -minCount 5 -neg 5 -loss ns -bucket 2000000 -thread 1 -t 1e-3 -lrUpdateRate 100

echo $model_full_path
./evaluate.sh $model_full_path