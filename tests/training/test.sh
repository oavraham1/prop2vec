#!/bin/bash

input="wiki_10k_wlm"
output="model.tmp"
ref="wiki_10k_wlm.vec"

./../../training/fasttext skipgram -input ../tests/training/$input -output ../tests/training/$output -lr 0.025 -dim 200 -ws 2 -epoch 5 -minCount 5 -neg 5 -loss ns -bucket 2000000 -minn 0 -maxn 1 -thread 1 -t 1e-3 -lrUpdateRate 100
cmp --silent $ref $output || echo "training output has changed"