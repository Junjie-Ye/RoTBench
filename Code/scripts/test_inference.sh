export CUDA_VISIBLE_DEVICES=0
export PYTHONPATH=./

python RoTBench/Code/Inference/inference_pipeline.py \
    --backbone_model toolllama \
    --model_path \
    --max_observation_length 1024 \
    --method tool \
    --input_query_file \
    --output_answer_file \
    --max_turn -1 \
    --history_sample 