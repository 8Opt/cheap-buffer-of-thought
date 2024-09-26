"""Define agent using OPENAI's API"""

import time

try:
    import openai

except ImportError as ie:
    raise ImportError("`openai` is not installed. Please try `pip install openai`!") from ie

from src.base import Generator

class OpenAIGenerator(Generator):
    def __init__(self, api_key, model_name, n=8, max_tokens=512, temperature=0.7, top_p=1, frequency_penalty=0.0, presence_penalty=0.0, stop=['\n\n\n'], wait_till_success=False):
        super().__init__(api_key, model_name)
        self.n = n
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        self.stop = stop
        self.wait_till_success = wait_till_success
        self.client = openai.OpenAI(api_key=api_key)
        self.model_name = model_name

    @staticmethod
    def parse_response(response):
        to_return = []
        for _, g in enumerate(response['choices']):
            text = g['text']
            logprob = sum(g['logprobs']['token_logprobs'])
            to_return.append((text, logprob))
        texts = [r[0] for r in sorted(to_return, key=lambda tup: tup[1], reverse=True)]
        return texts

    def generate(self, query, system_prompt=None, text_return=True, **kwargs):
        """
        Run the model with the given prompt and system prompt.

        Args:
        - prompt (str): The user's input.
        - system_prompt (str, optional): The system prompt. Defaults to None.
        - **kwargs: Additional keyword arguments to pass to the OpenAI client.

        Returns:
        - str: The model's response.
        """
        if system_prompt:
            messages = [{"role": "system", "content": system_prompt},
                        {"role": "user", "content": query}]
        else:
            messages = [{"role": "user", "content": query}]

        completion = self.client.chat.completions.create(
        model=self.model_name,
        messages=messages,
        stream=True,
        **kwargs,
        )
        if text_return: 
            response = self.parse_response(completion)
        return response
