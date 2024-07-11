data_dir=/work/wangjh/ruc_cell2location

export CUDA_VISIBLE_DEVICES=0

# nohup python train.py \
#     --metadata "$data_dir/LDX_all_meta.csv" \
#     --count-matrix-h5ad "$data_dir/LDX_all.h5ad" \
#     --spatial "$data_dir/all_count_data" \
#     --regression-model "./model/reference_signatures"
# exit

# nohup python train.py \
#     --ranks 0 1 2 3 4 5 6 7 8 9 \
#     --metadata "$data_dir/LDX_all_meta.csv" \
#     --count-matrix-h5ad "$data_dir/LDX_all.h5ad" \
#     --spatial "$data_dir/all_count_data" \
#     --regression-model "./model/reference_signatures" >device0.log 2>&1 &

export CUDA_VISIBLE_DEVICES=0

nohup python train.py \
    --ranks 12 13 14 15 \
    --metadata "$data_dir/LDX_all_meta.csv" \
    --count-matrix-h5ad "$data_dir/LDX_all.h5ad" \
    --spatial "$data_dir/all_count_data" \
    --regression-model "./model/reference_signatures" >device0-1.log 2>&1 &

nohup python train.py \
    --ranks 16 17 18 19 \
    --metadata "$data_dir/LDX_all_meta.csv" \
    --count-matrix-h5ad "$data_dir/LDX_all.h5ad" \
    --spatial "$data_dir/all_count_data" \
    --regression-model "./model/reference_signatures" >device0-2.log 2>&1 &
