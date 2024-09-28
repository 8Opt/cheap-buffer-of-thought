import json
import argparse

def evaluate_task(task_name, benchmark_path, test_path):
    """Evaluates the performance of a model on a given task.

    Args:
        task_name (str): The name of the task.
        benchmark_path (str): The path to the benchmark data.
        test_path (str): The path to the test results.

    Returns:
        tuple: A tuple containing the total number of test cases, the number of correct answers, and the accuracy.
    """

    benchmark_data = []
    test_data = []

    # Load benchmark and test data
    with open(benchmark_path) as f:
        for line in f:
            benchmark_data.append(json.loads(line)['target'])
    with open(test_path) as f:
        for line in f:
            result = json.loads(line)['result']
            if task_name == 'gameof24':
                result = result.split('=')[0]
            test_data.append(result)

    # Calculate accuracy
    correct = 0
    for i in range(len(test_data)):
        if test_data[i] == benchmark_data[i]:
            correct += 1

    return len(test_data), correct, correct / len(test_data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--task_name', type=str, default='gameof24', choices=['gameof24', 'checkmate', 'wordsorting'])
    parser.add_argument('--test_path', type=str)
    args = parser.parse_args()

    task_name = args.task_name
    test_path = args.test_path

    benchmark_path_dict = {
        'gameof24': 'benchmarks/gameof24.jsonl',
        'checkmate': 'benchmarks/CheckmateInOne.jsonl',
        'wordsorting': 'benchmarks/word_sorting.jsonl'
    }

    test_path_dict = {
        'gameof24': 'test_results/BoT_gameof24.jsonl',
        'checkmate': 'test_results/BoT_checkmate.jsonl',
        'wordsorting': 'test_results/BoT_wordsorting.jsonl'
    }

    benchmark_path = benchmark_path_dict[task_name]
    test_path = test_path_dict[task_name]

    total, correct, accuracy = evaluate_task(task_name, benchmark_path, test_path)
    print(f'Total number: {total}, Correct number: {correct}, Accuracy: {accuracy}')