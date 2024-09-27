echo "Running experiment ..."
python run_benchmarks.py    --task_name='gameof24' \
                            --provider='gemini'   \
                            --api_key='input your API key here if you want to use GPT-4' \
                            --model_id='the model ID of GPT-4 or the path to your local LLM'

echo "Validating ..."
python validate_results.py  --task_name 'gameof24' \
                            --test_path 'The path to the .jsonl file you want to validate'