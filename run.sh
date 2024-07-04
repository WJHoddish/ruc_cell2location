#!/bin/bash
clear

# env
source ~/anaconda3/etc/profile.d/conda.sh
conda activate cell2loc_env

# pipeline
python h5ad.py \
    --count "./LDX_all.csv"
