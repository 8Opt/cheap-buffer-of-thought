# cheap-buffer-of-thought

## Introduction

This repository offers a fresh take on the code from [the original Buffer-of-Thought implementation](https://github.com/YangLing0818/buffer-of-thought-llm). While the original leveraged OpenAI as the reasoning LLM, this version prioritizes diversity. Here's the reasoning behind this choice:

1. Exploration of Alternatives: By not relying solely on OpenAI, this repository opens the door to exploring other LLMs with different strengths and weaknesses. This allows for a more comprehensive understanding of reasoning capabilities within large language models.
2. Potential for Bias Mitigation: Different LLMs are trained on diverse datasets, potentially leading to a wider range of perspectives and reduced bias in reasoning outputs.
3. Flexibility and Adaptability: This code's ability to work with various LLMs allows users to tailor the reasoning process to specific tasks and desired outcomes.


## Roadmaps

- [ ] Integrating Leading Cloud-Based LLM Services (OpenAI, Cohere, Gemini, SambaNova, Groq).
- [ ] Integrating On-Premise LLM Solutions (Ollama, HuggingFace (tiny models, small models, large models)). 
- [ ] Adding more templates. 


## Evaluation with Buffer of Thoughts

### 1. Benchmarks 

For now, we release our demo version of BoT based on three different benchmarks:

- **The Game of 24** from [Yao et al., 2023](https://github.com/princeton-nlp/tree-of-thought-llm)
- **Checkmate-in-One** from [the BIG-Bench suite](https://github.com/google/BIG-bench/tree/main) [(BIG-Bench authors, 2023)](https://arxiv.org/abs/2206.04615)
- **Word Sorting** from [BIG-Bench Hard](https://github.com/suzgunmirac/BIG-Bench-Hard) ([Suzgun et al., 2023](https://arxiv.org/abs/2210.09261); [BIG-Bench authors, 2023](https://github.com/google/BIG-bench/tree/main))

### 2. Meta Buffer

For each task, we choose one thought template sampled from our meta-buffer library. **Stay tuned for our complete meta-buffer library update!**

### 3. Quick Start

First, set up the environment:

```bash
git clone https://github.com/8Opt/cheap-buffer-of-thought
cd cheap-buffer-of-thought
conda create -n BoT python==3.9 
pip install -r requirements.txt
```

#### 3.1. Running on Three Benchmarks

Our BoT is easy to use. Just run:

```bash
python run_benchmarks.py --task_name 'gameof24' --api_key 'input your API key here if you want to use GPT-4' --model_id 'the model ID of GPT-4 or the path to your local LLM'
```

Here, **--task_name** could be one of gameof24, checkmate, wordsorting.

The **--api_key** is required if you want to use GPT-series; if not, you can skip it.

The **--model_id** should be the model ID of GPT-series like gpt-4o, gpt-4-turbo, or the path to your local LLM if you do not set **--api_key**.

The data for these three tasks are located in the `/benchmarks` directory.

The results generated during the experiment are stored in the `/test_results` directory.

#### 3.2. Validate the Test Results

Run the command below to validate the test results of our BoT:

```python
python validate_results.py --task_name 'gameof24' --test_path 'The path to the .jsonl file you want to validate'
```

This will print out the accuracy of the selected task on your relevant .jsonl file.

---

You guys can visit me via: [GitHub](https://github.com/MinLee0210) | [LinkedIn](www.linkedin.com/in/minhle007) | Medium | [Substack](https://minhleduc.substack.com/) 
Or contact me via: 
+ Gmail: minh.leduc.0210@gmail.com