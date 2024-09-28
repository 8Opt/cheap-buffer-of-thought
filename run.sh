#!/bin/bash

api_key=$(printenv GROQ_API_KEY)

echo "Running experiment ..."
python run_benchmarks.py    --task_name="gameof24" \
                            --provider="groq"   \
                            --api_key="$api_key" \
                            --model_name="llama-3.2-1b-preview"\
                            --clean_response=True

# You have to change the `--test_path` according to your test
# echo "Validating ..."
# python validate_results.py  --task_name 'gameof24' \
#                             --test_path 'The path to the .jsonl file you want to validate'