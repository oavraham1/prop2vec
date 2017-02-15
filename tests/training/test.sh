#!/bin/bash

ref=$PWD/wiki_10k_wlm.vec
input=$PWD/wiki_10k_wlm
output=$PWD/model.tmp

(cd "../../training"; make; ./fasttext skipgram -input $input -output $output -lr 0.025 -dim 200 -ws 2 -epoch 5 -minCount 5 -neg 5 -loss ns -bucket 2000000 -thread 1 -t 1e-3 -lrUpdateRate 100)
cmp --silent $ref $output.vec || echo "training output has changed"