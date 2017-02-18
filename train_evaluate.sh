#!/bin/bash

corpus_processed=$1
model=$corpus_processed.vec

./training/fasttext skipgram -input $corpus_processed -output $corpus_processed -props "w+l+m" -lr 0.025 -dim 200 -ws 2 -epoch 5 -minCount 5 -neg 5 -loss ns -bucket 2000000 -thread 1 -t 1e-3 -lrUpdateRate 100

./evaluate.sh $model