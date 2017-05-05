#!/bin/bash

script_dir=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
input_file_url="https://www.dropbox.com/s/d7r0a0pvenm5oak/wiki1m"
input_file=$script_dir/${input_file_url##*/}

if [ ! -f $input_file ]
then
  wget -c $input_file_url
fi

./preprocess_train_evaluate.sh $input_file