#!/bin/bash

ref=$PWD/wiki_10k_wlm
input=$PWD/wiki_10k_conll
output=$PWD/wiki_10k_wlm.tmp

(cd "../../preprocessing"; python preprocess.py -i $input -o $output)
cmp --silent $ref $output || echo "preprocessing output has changed"