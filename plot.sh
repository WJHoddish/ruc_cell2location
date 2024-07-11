#!/bin/bash
clear

# env
source ~/anaconda3/etc/profile.d/conda.sh
conda activate cell2loc_env

python plot_main.py
