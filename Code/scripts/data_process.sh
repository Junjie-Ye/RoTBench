# tranform clean_data to slight/medium/heavy/union_data
python RoTBench/Code/Data_Process/transform_process.py --origin_file $input_file --output_dir $output_dir

# adapt a dataset to NexusRaven-Prompt
python RoTBench/Code/Data_Process/NexusRaven_Prompt.py --version $version --origin_file $origin_file --raven_file $raven_file
