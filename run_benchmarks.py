import json
import argparse
import os
import datetime

from src.pipeline import BoT

def get_user_prompt(task_name):
    """
    Retrieves the user prompt based on the specified task.

    Args:
        task_name (str): The name of the task.

    Returns:
        str: The user prompt for the task.
    """
    benchmark_dict = {
        'gameof24': """
    Let's play a game called 24. You'll be given four integers, and your objective is to use each number only once, combined with any of the four arithmetic operations (addition, subtraction, multiplication, and division) and parentheses, to achieve a total of 24. For example, if the input is 4, 7, 8, and 8, the output   
    could be 7 * 8 - 4 * 8 = 24. You only need to find one feasible solution!
    Input:
    """,
        'checkmate': """
    Given a series of chess moves written in Standard Algebraic Notation (SAN), determine the next move that will result in a checkmate.   

    Input: 
    """,
        'wordsorting': """
    Sort a list of words alphabetically, placing them in a single line of text separated by spaces.
    Input:
    """
    }
    return benchmark_dict.get(task_name)

def get_benchmark_path(task_name): 
    path_dict = {

        'gameof24':'benchmarks/gameof24.jsonl',

        'checkmate':'benchmarks/CheckmateInOne.jsonl',

        'wordsorting':'benchmarks/word_sorting.jsonl'

    }
    return path_dict.get(task_name)

def run_task(task_name, api_key, model_name, provider):
    """
    Runs the specified task using the provided configuration.

    Args:
        task_name (str): The name of the task.
        api_key (str): The API key for the chosen provider (if applicable).
        model_name (str): The model name to use.
        provider (str): The provider of the large language model.
    """
    now = datetime.datetime.now()
    timestamp_str = now.strftime("%Y-%m-%d-%H:%M:%S")
    output_dir = 'test_results'

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    user_prompt = get_user_prompt(task_name)

    buffer_of_thought = BoT(
        query=None,
        problem_id=0,  # Assuming problem_id is not required in this context
        provider=provider,
        api_key=api_key,
        model_name=model_name,
        need_check=True
    )

    path = get_benchmark_path(task_name)
    for line in open(path):
        query = json.loads(line)['input']
        user_input = user_prompt + query
        buffer_of_thought.update_query(user_input)
        result = buffer_of_thought.generate()

        # if clean_response:
        #     result = clean(result)

        json_result = {'input': query, 'result': result}
        with open(f'./{output_dir}/BoT_{provider}_{model_name}_{task_name}_{timestamp_str}.jsonl', 'a+', encoding='utf-8') as file:
            print('writing to test_result')
            json_str = json.dumps(json_result)
            file.write(json_str + '\n')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--task_name', type=str, default='gameof24', choices=['gameof24', 'checkmate', 'wordsorting'])
    parser.add_argument('--provider', default='ollama', type=str, help='Input your provider here', choices=['cohere', 'openai', 'sambanova', 'gemini', 'groq', 'ollama'])
    parser.add_argument('--api_key', default=None, type=str, help='Input your API key here')
    parser.add_argument('--model_name', type=str, default='gpt-4o', help='Input model id here, if use local model, input the path to the local model')
    # parser.add_argument('--clean_response', type=bool, default=True, help="Responses from LLM may contain many whitespaces and unexpected symbols for the result, this method helps to clean those out")
    args = parser.parse_args()

    run_task(args.task_name, args.api_key, args.model_name, args.provider)