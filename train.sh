export CUDA_VISIBLE_DEVICES=1

python train.py \
    --metadata "./data/LDX_all_meta.csv" \
    --count-matrix-h5ad "./data/LDX_all.h5ad" \
    --regression-model "./model/reference_signatures"
