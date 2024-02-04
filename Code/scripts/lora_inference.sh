export CUDA_VISIBLE_DEVICES=0
export PYTHONPATH=./

python ./Code/Inference/inference_pipeline.py \
    --backbone_model tool \
    --model_path /mnt/data/Llama-2/hf/Llama-2-7b-hf\
    --lora \
    --lora_path /mnt/data/sft_document_avg_english_5e-5_lora\
    --max_observation_length 1024 \
    --method tool \
    --input_query_file ./Data/First_Turn/clean.json\
    --output_answer_file ./lora_test_result.jsonl\
    --max_turn -1 \
    --history_sample 1