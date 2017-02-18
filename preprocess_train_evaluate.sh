#!/bin/bash

corpus_conll=$1
corpus_processed=${corpus_conll}_processed

python preprocessing/preprocess.py -i $corpus_conll -o $corpus_processed

./train_evaluate.sh $corpus_processed