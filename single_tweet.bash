#!/bin/bash

bash
export PATH="~/anaconda3/bin:$PATH"
source activate markov
python ~/Documents/MarkovFun/src/TwitterBot.py &
